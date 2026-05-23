import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from ..db.database import get_connection

router = APIRouter()

# ✅ FIXED: Read SECRET_KEY from environment variable for security
# Set JWT_SECRET_KEY in your Render environment variables
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "MEMORAAI_SUPER_SECRET_CHANGE_IN_PRODUCTION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------
# Schemas
# -----------------------------
class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# -----------------------------
# Password Helpers
# -----------------------------
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# -----------------------------
# JWT Token Creation
# -----------------------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# -----------------------------
# Register Endpoint
# -----------------------------
@router.post("/register")
def register(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (user.email, hashed)
        )
        conn.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        conn.rollback()
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="Email already registered")
        raise HTTPException(status_code=500, detail="Registration failed")
    finally:
        cursor.close()
        conn.close()


# -----------------------------
# Login Endpoint
# -----------------------------
@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, password FROM users WHERE email=?",
            (user.email,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user_id, hashed = row
        if not verify_password(user.password, hashed):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token({"sub": str(user_id)})
        return {"access_token": token, "token_type": "bearer"}
    finally:
        cursor.close()
        conn.close()
