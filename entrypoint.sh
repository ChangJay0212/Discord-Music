#!/bin/bash
set -e

# 匯入環境變數
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# 執行機器人
exec python bot.py
