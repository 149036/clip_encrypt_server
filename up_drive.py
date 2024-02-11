import requests
import json


def upload_to_google_drive(
    video_path="",
    target_name="",
    access_token="",
    drive_folder_id="",
):

    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "name": target_name,
        "parents": [drive_folder_id],
    }
    files = {
        "data": ("metadata", json.dumps(params), "application/json; charset=UTF-8"),
        "file": open(video_path, "rb"),
    }
    response = requests.post(
        url="https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files,
    )
    print(response.json())
