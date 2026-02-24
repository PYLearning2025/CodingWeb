# 1. 使用輕量級 Python 映像檔
FROM python:3.11-slim

# 2. 設定環境變數
# 確保 Python 輸出直接印到 Cloud Run 日誌，方便排錯
ENV PYTHONUNBUFFERED True
# 將 /app 加入 PYTHONPATH，確保 app.py 能抓到 api/ 等子目錄的模組
ENV PYTHONPATH=/app
# 設定預設埠號
ENV PORT 8080

# 3. 設定工作目錄
# 在容器內建立一個乾淨的根目錄，建議使用 /app 避免混淆
WORKDIR /app

# 4. 安裝系統依賴 (選用)
# 如果您的 mongodb.py 或其他模組需要編譯環境，取消下方註解
# RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

# 5. 複製依賴清單並安裝
# 由於 Cloud Build 已將上下文設為 backend/，這裡的 . 就是您的 backend 目錄
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 複製後端程式碼
# 包含 app.py, api/, models/ 等所有內容
COPY . .

# 7. 啟動命令
# 根據您的目錄，主程式是 app.py，FastAPI 實例名是 app
# 使用 0.0.0.0 讓外部請求能進到容器
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]