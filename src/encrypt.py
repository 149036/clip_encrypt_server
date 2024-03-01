import subprocess
from src import clear


def aes_256_cbc(
    normal_files,
    dl_path,
    user_path,
):
    print("encrypt : start")
    for target in normal_files:
        target_path = dl_path + "/" + target
        output_path = user_path + "/encrypted/encrypted-" + target

        subprocess.run(
            [
                "openssl",
                "enc",
                "-e",
                "-aes-256-cbc",
                "-a",
                "-salt",
                "-k",
                "password",
                "-pbkdf2",
                "-in",
                target_path,
                "-out",
                output_path,
            ],
            check=True,
        )

        # キャシュの開放
        clear.cache()

        print(f"encrypted : {target}")
    print("encrypt : end")
