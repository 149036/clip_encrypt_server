import subprocess


def cache():
    # キャシュの開放
    cmd = "echo 1 | sudo tee /proc/sys/vm/drop_caches"
    subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        check=True,
    )
