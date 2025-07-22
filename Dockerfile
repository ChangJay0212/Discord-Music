FROM python:3.10-slim

# 安裝 ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# 建立工作目錄
WORKDIR /app

# 複製檔案
COPY requirements.txt ./
RUN pip install -U yt-dlp
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 設定環境變數
ENV PYTHONUNBUFFERED=1

# 啟動入口
RUN chmod +x entrypoint.sh
ENTRYPOINT ["bash", "entrypoint.sh"]
