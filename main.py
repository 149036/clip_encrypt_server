import os, subprocess, json
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import configparser

from src import yt_dlp
from src import up_drive
from src import _crypt

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


@app.post("/drive")
async def drive(drive: Drive):
    if drive.drive_folder_id == "":
        return {"message": "no drive folder id"}
    if drive.video_url == "":
        return {"message": "no video url"}
    if drive.access_token == "":
        return {"message": "no access token"}



    drive_folder_id = drive.drive_folder_id
    video_url = drive.video_url
    access_token = drive.access_token

    # config.iniを読み込む
    config_ini = configparser.ConfigParser()
    config_ini.read("config.ini", encoding="utf-8")

    user_path = f"./videos/drive-{os.urandom(4).hex()}"

    # projectroot/videos 配下に drive-{user名}/{encrypted,normal} のディレクトリを作る
    print(f"mkdir : {user_path}/encrypted")
    print(f"mkdir : {user_path}/normal")
    cmd = f"mkdir -p {user_path}/encrypted {user_path}/normal"
    subprocess.run(cmd.split(), check=True)

    # yt-dlp アップデート
    yt_dlp.update()

    # 動画を dl_path配下に ダウンロード
    # config.ini, [DEFAULT] tor=1 なら tor を使う
    yt_dlp.dl(
        user_path=user_path,
        video_url=video_url,
        config_ini=config_ini,
    )

    # dl_path配下のファイル一覧のリスト [a.mp4,...]
    dl_path = user_path + "/normal"
    normal_files = os.listdir(dl_path)

    # normal/* のファイルすべて暗号化
    _crypt.aes_256_cbc(
        normal_files=normal_files,
        dl_path=dl_path,
        user_path=user_path,
    )

    # google drive にencrypted/* のファイルすべてアップロード
    up_drive.up(
        user_path=user_path,
        drive_folder_id=drive_folder_id,
        access_token=access_token,
    )

    # user_pathフォルダを削除
    # cmd = f"rm -rf {user_path}"
    # subprocess.run(cmd.split(), check=True)
    # print(f"removed : {user_path}")

    return {"message": "finish"}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=7999, log_level="debug")
