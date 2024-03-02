import datetime
import json
import os
import subprocess
import mimetypes

from src import clear


def up(
    user_path,
    drive_folder_id,
    access_token,
    up_target_path,
):
    """google drive にtarget/* のファイルすべてアップロード

    Args:
        user_path (str)
        drive_folder_id (str)
        access_token (str)
        up_target_path (str)
    """

    targets = os.listdir(up_target_path)

    for target in targets:
        target_path = up_target_path + "/" + target
        print(f"target_path : {target_path}")

        metadata_path = gen_metadata(
            user_path,
            target,
            target_path,
            drive_folder_id,
        )

        print("upload : start")
        print(f"{datetime.datetime.now()} : upload : start")
        result = subprocess.run(
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
            capture_output=True,
            text=True,
        )

        if "error" in result.stdout:
            print("upload failed")
            print(result.stdout)
        clear.cache()

        print(f"uploaded :{target}")

    print(f"{datetime.datetime.now()} : upload : end")


def gen_metadata(
    user_path,
    target,
    target_path,
    drive_folder_id,
):
    """
    google drive にアップロードするときのmetadata.jsonを生成する

    Args:
        user_path (str):
        target (str):
        target_path (str):
        drive_folder_id (str):

    Returns:
        str: metadata.json の path
    """
    # metadata.json 生成
    print("gen_metadata : start")
    metadata_path = f"{user_path}/metadata.json"
    with open(metadata_path, "w") as f:
        param = {
            "name": target,
            "mimeType": mimetypes.guess_type(target_path)[0],
            "parents": [drive_folder_id],
        }
        f.write(json.dumps(param))
    print("gen_metadata : end")
    return metadata_path


