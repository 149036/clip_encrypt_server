# yt-dlp アップデート
import subprocess

from src import clear


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

    #### yt-dlp command
    flat_playlist = 1
    limit_rate = 100
    concurrent_fragments = 1
    cmd = f"""
        yt-dlp
        {video_url}
        --paths {dl_path}
        --id
        --flat-playlist {flat_playlist}
        --limit-rate {limit_rate}M
        --concurrent-fragments {concurrent_fragments}
    """
    # -r, --limit-rate RATE # Maximum download rate in bytes per second, e.g. 50K or 4.2M
    # (default (--no-flat-playlist)) Do not extract the videos of a playlist, only list them
    # -N, --concurrent-fragments N #   Number of fragments of a dash/hlsnative video that should be downloaded concurrently (default is 1)
    # f"--max-downloads {NUMBER}", # Abort after downloading NUMBER files

    if int(config_ini.get("DEFAULT", "tor")):
        # tor ture
        print("tor : true")
        print("tor : start")
        tor = subprocess.Popen(["tor"])
        cmd += " --proxy socks5://127.0.0.1:9050"

    print(cmd.split())
    result = subprocess.run(
        cmd.split(),
        capture_output=True,
        text=True,
        check=True,
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

    # キャシュの開放
    clear.cache()

    return True
