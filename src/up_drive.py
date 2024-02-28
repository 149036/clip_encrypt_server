import json
import os
import subprocess


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
        print("gen_metadata : start")
        metadata = f"{user_path}/metadata.json"
        with open(metadata, "w") as f:
            param = {
                "name": target,
                "mimeType": "video/mp4",
                "parents": [drive_folder_id],
            }
            f.write(json.dumps(param))
        target_path = encrypted_path + "/" + target
        print("gen_metadata : end")

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
                f"data=@{metadata};type=application/json;charset=UTF-8",
                "-F",
                f"file=@{target_path};type=text/plain",
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
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

        print(f"uploaded :{target}")
    print("upload : end")
