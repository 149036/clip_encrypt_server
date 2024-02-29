# yt-dlp アップデート
import subprocess



def update():
    print("yt-dlp : update")
    cmd = "yt-dlp -U"
    subprocess.run(cmd.split(), check=True)


def dl(
    user_path,
    video_url,
    config_ini,
) -> bool:
    # 動画を dl_path配下に ダウンロード
    print("yt-dlp : download : start")
    dl_path = user_path + "/normal"
    cmd = f"yt-dlp --paths {dl_path} {video_url} --id"

    if int(config_ini.get("DEFAULT", "tor")):
        # tor ture
        print("tor : true")
        print("tor : start")
        tor = subprocess.Popen(["tor"])
        cmd += " --proxy socks5://127.0.0.1:9050"

    print(cmd)
    result = subprocess.run(
        cmd.split(),
        # check=True,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("yt-dlp : download error")
        print(f"yt-dlp : stdout : {result.stdout}")
        print(f"yt-dlp : stderr : {result.stderr}")
        return False

    print("yt-dlp : download : end")

    if int(config_ini.get("DEFAULT", "tor")):
        print("tor : end")
        tor.kill()

    return True
