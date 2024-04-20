from base64 import b64encode
import os
import subprocess
from src import clear


def aes_256_cbc(
    normal_files,
    dl_path,
    user_path,
    config_ini,
):
    openssl = config_ini.get("DEFAULT", "openssl")
    pass_list = {}

    for target in normal_files:
        target_path = dl_path + "/" + target
        output_path = user_path + "/encrypted/encrypted-" + target

        if openssl == "openssl":
            password = os.urandom(32).hex()
            subprocess.run(
                [
                    "openssl",
                    "enc",
                    "-e",
                    "-aes-256-cbc",
                    "-a",
                    "-salt",
                    "-k",
                    password,
                    "-pbkdf2",
                    "-in",
                    target_path,
                    "-out",
                    output_path,
                ],
                check=True,
            )
            pass_list["encrypted-" + target] = password

        elif openssl == "libressl":
            key_bytes = os.urandom(32)
            iv_bytes = os.urandom(16)

            b64_key = b64encode(key_bytes).decode()
            b64_iv = b64encode(iv_bytes).decode()

            key = key_bytes.hex()
            iv = iv_bytes.hex()

            subprocess.run(
                [
                    "openssl",
                    "enc",
                    "-e",
                    "-aes-256-cbc",
                    "-base64",
                    "-nosalt",
                    "-p",
                    "-K",
                    key,
                    "-iv",
                    iv,
                    "-in",
                    target_path,
                    "-out",
                    output_path,
                ],
                check=True,
            )
            pass_list["encrypted-" + target] = {"key": b64_key, "iv": b64_iv}

        clear.cache()

    return pass_list
