from fastapi import APIRouter, HTTPException, status
from models.users import UserCreate
from api.mongodb import mongodb
from map import DATABASE, COLLECTION
from argon2 import PasswordHasher
from datetime import datetime

router = APIRouter()
ph = PasswordHasher()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    """
    Register a new user
    """
    # Check if email already exists
    existing_user = mongodb.get_data(
        DATABASE.ACCOUNT.value, 
        COLLECTION.USER.value, 
        {"email": user.email}, 
        limit=1
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Prepare user data
    user_data = user.dict()
    
    # Hash password
    user_data["password"] = ph.hash(user.password)
    
    # Set timestamps
    current_time = datetime.utcnow()
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
def login():
    # TODO: Login the user
    pass

@router.post("/logout")
def logout():
    # TODO: Logout the user
    pass