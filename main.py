import os, subprocess, json
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import configparser


app = FastAPI()

origins = ["https://localhost:7999"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Drive(BaseModel):
    drive_folder_id: str
    video_url: str
    access_token: str


@app.get("/")
async def root():
    return {"message": "hello"}


@app.post("/drive")
async def drive(drive: Drive):
    # config.ini
    config_ini = configparser.ConfigParser()
    config_ini.read("config.ini", encoding="utf-8")

    drive_folder_id = drive.drive_folder_id
    video_url = drive.video_url
    access_token = drive.access_token
    user_path = f"./videos/drive-{os.urandom(4).hex()}"

    # projectroot/videos 配下に drive-{user名}/{encrypted,normal} のディレクトリを作る
    cmd = f"mkdir -p {user_path}/encrypted {user_path}/normal"
    subprocess.run(
        cmd.split(),
        check=True,
    )

    # yt-dlp アップデート
    cmd = "yt-dlp -U"
    subprocess.run(
        cmd.split(),
        check=True,
    )

    # 動画を dl_path配下に ダウンロード
    dl_path = user_path + "/normal"
    cmd = f"yt-dlp --paths {dl_path} {video_url} --id"
    # tor ture
    if int(config_ini.get("DEFAULT", "tor")):
        tor = subprocess.Popen(["tor"])
        cmd += " --proxy socks5://127.0.0.1:9050"

    subprocess.run(cmd.split(), check=False)

    if int(config_ini.get("DEFAULT", "tor")):
        tor.kill()

    # dl_path配下のファイル一覧のリスト [a.mp4,...]
    normal_files = os.listdir(dl_path)

    # 暗号化
    for target in normal_files:
        target_path = dl_path + "/" + target
        output_path = user_path + "/encrypted/encrypted-" + target

        subprocess.run(
            [
                "openssl",
                "enc",
                "-e",
                "-aes-256-cbc",
                "-a",
                "-salt",
                "-k",
                "password",
                "-pbkdf2",
                "-in",
                target_path,
                "-out",
                output_path,
            ],
            check=True,
        )
        # キャシュの開放
        cmd = "echo 1 | sudo tee /proc/sys/vm/drop_caches"
        subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            check=True,
        )
        print(f"encrypted : {target}")

    # google drive にアップロード
    encrypted_path = user_path + "/encrypted"
    encrypted_files = os.listdir(encrypted_path)
    for target in encrypted_files:
        metadata = f"{user_path}/metadata.json"
        with open(metadata, "w") as f:
            param = {
                "name": target,
                "mimeType": "video/mp4",
                "parents": [drive_folder_id],
            }
            f.write(json.dumps(param))
        target_path = encrypted_path + "/" + target

        print(f"accesstoken : {access_token}")

        subprocess.run(
            [
                "curl",
                "-X",
                "POST",
                "-H",
                f"Authorization: Bearer {access_token}",
                "-F",
                f"data=@{metadata};type=application/json;charset=UTF-8",
                "-F",
                f"file=@{target_path};type=text/plain",
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            ],
            check=True,
        )

    # user_pathフォルダを削除
    # cmd = f"rm -rf {user_path}"
    # subprocess.run(cmd.split(), check=False)

    return {"message": "complete"}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=7999, log_level="debug")
