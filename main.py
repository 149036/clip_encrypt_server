import os, subprocess
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import configparser

from src import yt_dlp
from src import up_drive
from src import encrypt
from src import clear


class Model(BaseModel):
    drive_folder_id: str
    video_url: str
    access_token: str


from src import valid


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "hello"}


@app.post("/drive")
async def drive(model: Model):
    check = valid.Valid(model)

    if not check.result:
        return_msg = {"messge": "error"}
    else:
        drive_folder_id = model.drive_folder_id
        video_url = model.video_url
        access_token = model.access_token

        # config.iniを読み込む
        config_ini = configparser.ConfigParser()
        config_ini.read("config.ini", encoding="utf-8")

        user_path = f"./videos/drive-{os.urandom(4).hex()}"

        # projectroot/videos/drive-{user名}/normal ディレクトリを作る
        print(f"mkdir : {user_path}/normal")
        cmd = f"mkdir -p {user_path}/normal"
        subprocess.run(cmd.split(), check=True)

        # yt-dlp アップデート
        yt_dlp.update()

        # 動画を dl_path配下に ダウンロード
        # config.ini, [DEFAULT] tor=1 なら tor を使う
        # video_url が無効の場合 error
        # dl 失敗で error
        if not yt_dlp.dl(
            user_path=user_path,
            video_url=video_url,
            config_ini=config_ini,
        ):
            return_msg = {"message": "error"}
            return return_msg

        # dl_path配下のファイル一覧のリスト [a.mp4,...]
        dl_path = user_path + "/normal"
        normal_files = os.listdir(dl_path)

        if int(config_ini.get("DEFAULT", "encrypt")):
            # projectroot/videos/drive-{user名}/encrypted ディレクトリを作る
            print(f"mkdir : {user_path}/encrypted")
            cmd = f"mkdir -p {user_path}/encrypted"
            subprocess.run(cmd.split(), check=True)

            # normal/* のファイルすべて暗号化
            encrypt.aes_256_cbc(
                normal_files=normal_files,
                dl_path=dl_path,
                user_path=user_path,
            )
            up_target_path = user_path + "/encrypted"
        else:
            up_target_path = user_path + "/normal"

        # google drive にencrypted/* のファイルすべてアップロード
        up_drive.up(
            user_path=user_path,
            drive_folder_id=drive_folder_id,
            access_token=access_token,
            up_target_path=up_target_path,
        )

        # user_pathフォルダを削除
        cmd = f"rm -rf {user_path}"
        subprocess.run(cmd.split(), check=True)
        print(f"removed : {user_path}")

        return_msg = {"message": "finish"}

    # キャッシュクリア
    clear.cache()
    return return_msg


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=7999, log_level="debug")
