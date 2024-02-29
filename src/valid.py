import requests
from main import Model


class Valid:
    def __init__(self, model: Model):
        print("Valid : start")
        self.result = self.run(
            model.drive_folder_id,
            model.video_url,
            model.access_token,
        )
        print("Valid : end")

    def run(self, drive_folder_id, video_url, access_token):
        if not self.hasValue(drive_folder_id):
            return False
        if not self.hasValue(video_url):
            return False
        if not self.hasValue(access_token):
            return False
        if not self.checkPermission(drive_folder_id, access_token):
            return False

        return True

    # 値が 空文字(初期値) の場合 False
    def hasValue(self, value: str) -> bool:
        if value == "":
            print('value is ""')
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
