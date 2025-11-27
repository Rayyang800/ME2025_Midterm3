#!/bin/bash

# ====== 你需要修改的地方 ======
GIT_URL="https://github.com/Rayyang800/ME2025_Midterm3.git"   # <--- 改成你的 Git 位置
APP_DIR="$HOME/ME2025_Midterm3"                      # clone 後放的目錄
PYTHON="python3"                                     # Ubuntu 20.04 預設 python3
# ======================================

cd "$HOME"

# =============== 首次執行: clone =================
if [ ! -d "$APP_DIR" ]; then
    echo "[1/4] 第一次執行：clone repository ..."
    git clone "$GIT_URL" "$APP_DIR"
fi

cd "$APP_DIR"

# =============== 建立 venv ========================
if [ ! -d ".venv" ]; then
    echo "[2/4] 建立虛擬環境 .venv ..."
    $PYTHON -m venv .venv
fi

echo "[3/4] 啟動虛擬環境 ..."
source .venv/bin/activate

# =============== 第二次以後執行：更新 ==============
if [ -d ".git" ]; then
    echo "[4/4] 拉取專案最新版本 (git pull) ..."
    git pull
fi

# =============== 安裝/更新套件 =====================
echo "檢查並安裝缺少的套件 (pip install -r requirements.txt) ..."
pip install --upgrade pip
pip install -r requirements.txt

# =============== 殺掉舊的 Flask ===================
echo "若 app.py 已在背景執行，嘗試關閉 ..."
pkill -f "python.*app.py" 2>/dev/null

# =============== 重新啟動 app.py ==================
echo "啟動 Flask 應用程式 ..."
nohup python3 app.py > flask.log 2>&1 &

echo "部署完成！Flask 已在背景執行"
echo "Log 檔案：$APP_DIR/flask.log"
