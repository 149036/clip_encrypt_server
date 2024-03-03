import subprocess
import requests
from src import model


class Valid:
    def __init__(self, model: model.Model):
        """バリデート

        Args:
            model (model.Model): _description_
        """
        print("Valid : start")
        self.result = self.run(model.drive_folder_id, model.video_url, model.access_token, model.encryption)
        print("Valid : end")

    def run(
        self,
        drive_folder_id,
        video_url,
        access_token,
        encryption,
    ) -> bool:
        """実行する関数

        Args:
            drive_folder_id (str)
            video_url (str)
            access_token (str)
            encrypt (bool)

        Returns:
            bool: 正しい値ならば True
        """

        if not self.hasValue(drive_folder_id):
            print('error : drive_folder_id is ""')
            return False
        if not self.hasValue(video_url):
            print('error : video_url is ""')
            return False
        if not self.hasValue(access_token):
            print('error : access_token is ""')
            return False
        if not self.hasValue(encryption):
            print('error : encryption is ""')
            return False
        if not self.checkPermission(drive_folder_id, access_token):
            return False
        if not self.is_downloadable(video_url):
            return False

        return True

    # 値が 空文字(初期値) の場合 False
    def hasValue(self, value: str) -> bool:
        if value == "":
            return False
        return True

    # フォルダのパーミッションを確認する
    # アクセストークンが有効でなければ error
    # drive_folder  がなければ error

    # drive_folder が 共有の場合
    # 共有されている & 編集可 の場合 True
    def checkPermission(self, drive_folder_id, access_token):
        url = f"https://www.googleapis.com/drive/v3/files/{drive_folder_id}/permissions?access_token={access_token}"
        data = requests.get(url).json()
        if "error" in [i for i in data]:
            print("Error : ")
            print(data)
            return False
        return True

    def is_downloadable(self, video_url):
        cmd = f"yt-dlp {video_url} --simulate --skip-download --verbose --id"
        res = subprocess.run(cmd.split())
        if res.returncode != 0:
            print("Error : video is not downloadable")

            return False
        return True
