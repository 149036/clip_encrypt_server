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
    limit_rate = "100M"
    concurrent_fragments = 4

    #### yt-dlp command
    cmd = f"""
        yt-dlp
        --paths {dl_path}
        --id
        --limit-rate {limit_rate}
        --concurrent-fragments {concurrent_fragments}
        {video_url}
    """

    is_flat_list = True
    if is_flat_list:
        cmd += " --flat-playlist"
    # --throttled-rate RATE # Minimum download rate in bytes per second below which throttling is assumed and the video data is re-extracted, e.g. 100K
    # -r, --limit-rate RATE # Maximum download rate in bytes per second, e.g. 50K or 4.2M
    # --flat-playlist (default (--no-flat-playlist)) Do not extract the videos of a playlist, only list them
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
