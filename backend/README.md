# CodingWeb Backend

Backend service for the CodingWeb project, built with FastAPI and MongoDB.
本專案為 CodingWeb 的後端服務，使用 FastAPI 與 MongoDB 建構。

## Prerequisites / 前置需求

- Python 3.9+
- MongoDB

## Installation / 安裝步驟

1. **Create a virtual environment / 建立虛擬環境**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate   # Windows
   ```

2. **Install dependencies / 安裝依賴套件**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration / 設定

This project requires environment variables for configuration. You can set them in your terminal.
本專案需要透過環境變數進行設定，請在終端機中設定。

**Required Variables / 必填變數:**

- `MONGODB_URL`: MongoDB connection string / MongoDB 連線字串

**Example (macOS/Linux) / 範例:**

```bash
export MONGODB_URL="mongodb+srv://<username>:<password>@cluster.example.com/codingweb?retryWrites=true&w=majority"
```

## Running the Application / 啟動應用程式

Start the development server using Uvicorn:
使用 Uvicorn 啟動開發伺服器：

```bash
uvicorn app:app --reload
```

The server will start at `http://127.0.0.1:8000`.
伺服器將會在 `http://127.0.0.1:8000` 啟動。

## API Documentation / API 文件

Interactive API docs are available at:
互動式 API 文件可於以下連結查看：

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

