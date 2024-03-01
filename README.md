#

0.クライアントから google folder id と video url と access token を受け取る  
1.yt-dlp で動画をダウンロード 2.動画を暗号化  
3.google drive にアップ  
する API サーバー  

## 使用ツール

yt-dlp  
tor(option)

### 使い方

### linux

```sh
git clone https://github.com/149036/dl-crypt-drive-server.git
cd dl-crypt-drive-server
python3 -m venv venv
source venv/bin/active
pip install -r requirements.txt

python3 main.py
```

gunicorn daemon

```sh
gunicorn main:app --workers 4 --threads 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7999 --timeout 600 --daemon
```

or

```sh
chmod +x run.sh
./run.sh
```

daemon kill

```sh
ps aux | grep gunicorn
kill xxxx
```

### roadmap

並列ダウンロード(tor)  
ストリーム暗号  
メモリ足りない  
