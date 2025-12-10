from fastapi import APIRouter, HTTPException, status
from models.users import UserCreate, UserLogin, LoginResponse
from api.mongodb import mongodb
from map import DATABASE, COLLECTION
from argon2 import PasswordHasher
from datetime import datetime, timezone
from utils import create_access_token
router = APIRouter()
ph = PasswordHasher()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    """
    Register a new user

    Args:
        name: 使用者名稱
        email: 使用者email
        password: 使用者密碼
    
    Returns:
        dict: 註冊成功後的訊息
            {
                "message": "User registered successfully",
                "user_id": user_id
            }
    """
    user = mongodb.get_data(
        DATABASE.ACCOUNT.value, 
        COLLECTION.USER.value, 
        {"email": user.email}, 
        limit=1
    )

    # Prepare user data
    user_data = user.model_dump()
    
    # Hash password
    user_data["password"] = ph.hash(user.password)
    
    # Set timestamps
    current_time = datetime.now(timezone.utc)
    user_data["created_at"] = current_time
    user_data["updated_at"] = current_time
    
    # Convert Enums to values for MongoDB storage
    user_data["role"] = user.role.value
    user_data["status"] = user.status.value
    
    # Insert user into database
    user_id = mongodb.add_data(
        DATABASE.ACCOUNT.value, 
        COLLECTION.USER.value, 
        user_data
    )
    
    return {
        "message": "User registered successfully", 
        "user_id": user_id
    }

@router.post("/login")
def login(user: UserLogin):
    """
    Login a user

    Args:
        name: 使用者名稱
        email: 使用者email
        password: 使用者密碼
    
    Returns:
        dict: 登入成功後的訊息
            {
                "token": token
            }
    """
    existing_user = mongodb.get_data(
        DATABASE.ACCOUNT.value, 
        COLLECTION.USER.value, 
        {"name": user.name}, 
        limit=1
    )
    
    if not ph.verify(existing_user[0]["password"], user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )
    
    # Generate PASETO token
    access_token = create_access_token(
        data={
            "sub": user.name,
            "user_id": str(existing_user[0]["_id"]),
            "role": existing_user[0].get("role", "user")
        }
    )

    return {"token": access_token}

@router.post("/logout")
def logout():
    # TODO: Logout the user
    pass