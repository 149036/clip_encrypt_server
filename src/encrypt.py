import os
import subprocess
from base64 import b64encode

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

            key_b64 = b64encode(key_bytes).decode()
            iv_b64 = b64encode(iv_bytes).decode()

            key_hex = key_bytes.hex()
            iv_hex = iv_bytes.hex()

            cmd = f"""
                    openssl
                    enc
                    -e
                    -aes-256-cbc
                    -nosalt
                    -p
                    -K {key_hex}
                    -iv {iv_hex}
                    -in {target_path}
                    -out {output_path}
                    """

            subprocess.run(cmd.split(), check=True)
            pass_list["encrypted-" + target] = {"key": key_b64, "iv": iv_b64}

        clear.cache()

    return pass_list
