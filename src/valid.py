import subprocess
from typing import Optional

import requests

from src import model


class Valid:
    def __init__(self, model: model.Model):
        """バリデート

        Args:
            model (model.Model): _description_
        """
        print("Valid : start")
        print(model)
        self.result = self.__run(
            model.drive_folder_id, model.video_url, model.access_token, model.encryption
        )
        print("Valid : end")

    def __run(
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

        if (
            self.__hasValue(
                [
                    drive_folder_id,
                    video_url,
                    access_token,
                    encryption,
                ]
            )
            is None
        ):
            return False

        if not self.__checkPermission(drive_folder_id, access_token):
            return False
        if not self.__is_downloadable(video_url):
            return False

        return True

    # 値が 空文字(初期値) の場合 False
    def __hasValue(self, targets) -> Optional[str]:
        if "" in targets:
            return None
        return "ok"

    # フォルダのパーミッションを確認する
    # アクセストークンが有効でなければ error
    # drive_folder  がなければ error

    # drive_folder が 共有の場合
    # 共有されている & 編集可 の場合 True
    def __checkPermission(self, drive_folder_id, access_token):
        # url = f"https://www.googleapis.com/drive/v3/files/{drive_folder_id}/permissions?access_token={access_token}"
        # data = requests.get(url).json()
        # if "error" in [i for i in data]:
        #     print("Error : ")
        #     print(data)
        #     return False
        # return True
        url = f"https://www.googleapis.com/drive/v3/files/{drive_folder_id}/permissions?access_token={access_token}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return False

        try:
            data = response.json()
        except ValueError:
            print("Error: Response is not valid JSON")
            print(response.text)
            return False

        if "error" in data:
            print("Error:", data)
            return False

        return True

    def __is_downloadable(self, video_url):
        cmd = f"""
            yt-dlp {video_url}
            --simulate
            --skip-download
            --verbose
            --id
            --no-check-certificates
        """
        # "--check-formats", #--check-all-formats # Make sure formats are selected only from those that are actually downloadable
        # "-F", #-F, --list-formats # List available formats of each video. Simulate unless --no-simulate is used

        res = subprocess.run(cmd.split(), check=True)
        if res.returncode != 0:
            print("Error : video is not downloadable")

            return False
        return True
