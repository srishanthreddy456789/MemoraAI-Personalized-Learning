from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from ..db.database import cursor, conn

router = APIRouter()

# 🔐 Change this in production
SECRET_KEY = "MEMORAAI_SUPER_SECRET"
ALGORITHM = "HS256"

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
def create_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# -----------------------------
# Register Endpoint
# -----------------------------
@router.post("/register")
def register(user: UserCreate):

    hashed = hash_password(user.password)

    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (user.email, hashed)
        )
        conn.commit()
    except:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User created successfully"}


# -----------------------------
# Login Endpoint
# -----------------------------
@router.post("/login")
def login(user: UserLogin):

    cursor.execute(
        "SELECT id, password FROM users WHERE email=?",
        (user.email,)
    )
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user_id, hashed_password = row

    if not verify_password(user.password, hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token(user_id)

    return {"access_token": token}