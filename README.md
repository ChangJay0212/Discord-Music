# 🎵 Discord YouTube 音樂機器人

這是一個使用 Python 開發的 Discord 音樂機器人，能夠透過 `/play` 指令搜尋 YouTube 音樂或直接貼上網址播放。支援 cookie 驗證，可播放登入後才能觀看的影片（例如：年齡限制影片）。

---

## 📌 專案概要

- ✅ 支援 YouTube 搜尋與播放
- 🔐 支援使用 `cookies.txt` 播放登入影片
- 🧠 自動加入使用者所在語音頻道
- 🛠 可用 Docker 一鍵部署
- 🎮 簡單易懂的指令集 `/play`, `/pause`, `/resume`, `/stop`, `/leave`

---

## 🛠️ 安裝與執行步驟

### 📁 1. 準備環境

安裝以下必要工具：

- Python 3.10+
- `ffmpeg`（音訊播放必備）
- 取得 `cookies.txt`  
  → 安裝 Chrome 擴充套件 [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)，登入 YouTube 後匯出並命名為 `cookies.txt`。

建立 `.env` 檔案並填入你的 Discord Bot Token：

```env
    DISCORD_BOT_TOKEN=你的 Discord Token
```
### 🧪 2. 本地執行
```bash
    pip install -r requirements.txt
    python bot.py
```
### 🐳 3. 使用 Docker 執行
```bash
    docker build -t discord-music-bot .
    docker run --rm -it --env-file .env -v $(pwd)/cookies.txt:/app/cookies.txt discord-music-bot

```
## requirements.txt
```txt
    discord.py
    yt-dlp
    python-dotenv

```

## 🚀 Bot 指令集
| 指令               | 功能說明            |
| ---------------- | --------------- |
| `/join`          | 加入語音頻道          |
| `/play <關鍵字或網址>` | 播放指定 YouTube 音樂 |
| `/pause`         | 暫停播放            |
| `/resume`        | 繼續播放            |
| `/stop`          | 停止播放            |
| `/skip`          | 跳過       |        |
| `/leave`         | 離開語音頻道          |

## 📂 專案結構

``` bash
.
├── bot.py             # 主程式
├── .env               # 儲存 Discord Token
├── cookies.txt        # YouTube 的登入 cookie
├── Dockerfile         # Docker 建置腳本
└── requirements.txt   # Python 套件需求
```

## 📌 備註
* 若播放失敗且顯示「影片受限」或「無法存取」，請確認 cookies.txt 為有效且 為登入狀態。

* 支援 /play <關鍵字> 搜尋並自動播放第一筆結果，或直接貼上網址播放。