from fastapi import HTTPException
import logging
import sys

# 配置日志格式
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 使用者驗證錯誤
class InvalidCredentials(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)
        
        # 獲取錯誤訊息
        frame = sys._getframe(1)
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        func_name = frame.f_code.co_name
        
        logging.error(
            f"Authentication failed in {func_name}() at {filename}:{lineno} - {detail}"
        )