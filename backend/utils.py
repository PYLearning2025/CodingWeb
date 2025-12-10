from api.mongodb import mongodb
from map import DATABASE, COLLECTION
from argon2 import PasswordHasher
import pyseto
from pyseto import Key
from config import config

pwd_context = PasswordHasher()

def create_access_token(data: dict) -> str:
    """
    Generate a PASETO token without expiration
    """
    to_encode = data.copy()
    
    key = Key.new(version=4, purpose="local", key=config.PASETO_SECRET_KEY.encode())
    
    token = pyseto.encode(key, to_encode)
    return token.decode()

def check_email_exists(email: str, exclude_user_id: str = None) -> bool:
    """
    檢查 email 是否已存在
    
    Args:
        email: 要檢查的 email
        exclude_user_id: 排除的用戶 ID（用於更新時排除自己）
    
    Returns:
        True 如果 email 已存在，False 如果不存在
    """
    existing_users = mongodb.get_data(
        DATABASE.CLIENT_DATA.value, 
        COLLECTION.USERS.value, 
        email__eq=email
    )
    
    if not existing_users:
        return False
    
    # 如果是在更新用戶，排除自己
    if exclude_user_id:
        for user in existing_users:
            if user["_id"] != exclude_user_id:
                return True
        return False
    
    return True

def hash_password(password: str) -> str:
    """
    對密碼進行哈希加密
    
    Args:
        password: 原始密碼
    
    Returns:
        加密後的密碼哈希值
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    驗證密碼是否正確
    
    Args:
        plain_password: 原始密碼
        hashed_password: 加密後的密碼哈希值
    
    Returns:
        True 如果密碼正確，False 如果密碼錯誤
    """
    return pwd_context.verify(hashed_password, plain_password)
