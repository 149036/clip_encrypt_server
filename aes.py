# aes-256 動画
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


def gen():
    # 共通鍵生成
    key = os.urandom(32)
    print(f"共通鍵: {key.hex()}")

    # 初期化ベクトル(IV)生成
    iv = os.urandom(16)
    print(f"IV: {iv.hex()}")

    return key, iv


def encrypt(target_path, output_path, key, iv) -> None:

    # 動画ファイルの読み込み
    with open(target_path, "rb") as f_input:
        video_data = f_input.read()

    # AES-256 CBC 暗号化
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padded_video_data = video_data + b"\0" * (16 - len(video_data) % 16)  # PKCS#7パディング
    encrypted_video_data = encryptor.update(padded_video_data) + encryptor.finalize()

    # 暗号化された動画ファイルの書き込み
    with open(output_path, "wb") as f_output:
        f_output.write(iv + encrypted_video_data)


# def decrypt(key):

#     # 復号化
#     with open("encrypted_video.mp4", "rb") as f_input:
#         backend = default_backend()
#         iv = f_input.read(16)  # 最初の16バイトはIV
#         encrypted_video_data = f_input.read()

#     decryptor = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend).decryptor()
#     decrypted_video_data = decryptor.update(encrypted_video_data) + decryptor.finalize()

#     # PKCS#7パディングを除去
#     unpadded_video_data = decrypted_video_data.rstrip(b"\0")

#     # 復号化された動画ファイルの書き込み
#     with open("decrypted_video.mp4", "wb") as f_decrypted:
#         f_decrypted.write(unpadded_video_data)
