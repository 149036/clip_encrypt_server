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
    # google drive にtarget/* のファイルすべてアップロード

    # ["file1","file2"...]
    targets = os.listdir(up_target_path)

    for target in targets:
        target_path = up_target_path + "/" + target
        print(f"target_path : {target_path}")
        # metadata.json 生成
        metadata_path = gen_metadata(
            user_path,
            target,
            target_path,
            drive_folder_id,
        )

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
    target_path,
    drive_folder_id,
):
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
