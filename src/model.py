from pydantic import BaseModel


class Model(BaseModel):
    drive_folder_id: str
    video_url: str
    access_token: str
    encryption: bool
    crypt_algo: str
