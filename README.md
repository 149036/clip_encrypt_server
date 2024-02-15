0.クライアントから google folder id と 動画の url を受け取る
1.yt-dlp で動画をダウンロード 2.動画を暗号化
3.google drive にアップ
する API サーバー

### 使用ツール

yt-dlp
tor

### 使い方

linux

```sh
$ git clone https://github.com/149036/dl-crypt-drive-server.git
$ cd dl-crypt-drive-server
$ python3 -m venv venv
$ source venv/bin/active
$ pip install -r requirements.txt
$ python3 main.py
```

tor を使う場合は立ち上げておく

```sh
$ tor
```
