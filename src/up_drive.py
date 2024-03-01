from importlib import metadata
import json
import os
import subprocess
from src import clear


def up(
    user_path,
    drive_folder_id,
    access_token,
):
    # google drive にencrypted/* のファイルすべてアップロード
    print("upload")
    encrypted_path = user_path + "/encrypted"
    encrypted_files = os.listdir(encrypted_path)
    for target in encrypted_files:

        # metadata.json 生成
        metadata_path = gen_metadata(user_path, target, drive_folder_id)

        target_path = encrypted_path + "/" + target

        # upload
        print("upload : start")
        subprocess.run(
            [
                "curl",
                "-X",
                "POST",
                "-H",
                f"Authorization: Bearer {access_token}",
                "-F",
                f"data=@{metadata_path};type=application/json;charset=UTF-8",
                "-F",
                f"file=@{target_path};type=text/plain",
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            ],
            check=True,
        )

        # キャシュの開放
        clear.cache()

        print(f"uploaded :{target}")
    print("upload : end")


def gen_metadata(
    user_path,
    target,
    drive_folder_id,
):
    # metadata.json 生成
    print("gen_metadata : start")
    metadata_path = f"{user_path}/metadata.json"
    with open(metadata_path, "w") as f:
        param = {
            "name": target,
            "mimeType": "video/mp4",
            "parents": [drive_folder_id],
        }
        f.write(json.dumps(param))
    print("gen_metadata : end")
    return metadata_path
