import os, subprocess
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import configparser

import aes, up_drive


app = FastAPI()

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


@app.post("/drive/")
async def drive(drive: Drive):
    # config.ini
    config_ini = configparser.ConfigParser()
    config_ini.read("config.ini", encoding="utf-8")

    drive_folder_id = drive.drive_folder_id
    video_url = drive.video_url
    access_token = drive.access_token
    user_path = f"./videos/drive-{os.urandom(32).hex()}"

    # projectroot/videos 配下に drive-{user名}/{encrypted,normal} のディレクトリを作る
    cmd = f"mkdir -p {user_path}/encrypted {user_path}/normal"
    subprocess.run(cmd.split(), check=False)

    # yt-dlp アップデート
    cmd = "yt-dlp -U"
    subprocess.run(cmd.split(), check=False)

    # 動画を dl_path配下に ダウンロード
    dl_path = user_path + "/normal"
    cmd = f"yt-dlp --paths {dl_path} {video_url}"
    # tor ture
    if int(config_ini.get("DEFAULT", "tor")):
        cmd += " --proxy socks5://127.0.0.1:9050"
    subprocess.run(cmd.split(), check=False)

    # dl_path配下のファイル一覧のリスト [a.mp4,...]
    normal_files = os.listdir(dl_path)

    # 暗号化
    keys = []
    for target in normal_files:
        target_path = dl_path + "/" + target
        output_path = user_path + "/encrypted/encrypted-" + target
        key, iv = aes.gen()
        aes.encrypt(target_path, output_path, key, iv)
        keys.append({f"encrypted-{target}": {"key": key.hex()}})

    print(keys)

    # google drive にアップロード
    encrypted_path = user_path + "/encrypted"
    encrypted_files = os.listdir(encrypted_path)
    for target in encrypted_files:
        up_drive.upload_to_google_drive(
            video_path=encrypted_path + "/" + target,
            target_name=target,
            drive_folder_id=drive_folder_id,
            access_token=access_token,
        )

    # user_pathフォルダを削除
    cmd = f"rm -rf {user_path}"
    subprocess.run(cmd.split(), check=False)

    return keys


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=7999, log_level="debug")
