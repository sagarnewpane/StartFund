import os
from datetime import datetime, timedelta
from typing import Annotated

from auth import hash_password, verify_password
from database import users_collection
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from models import LoginRequest, UserCreate, UserInDB, UserPublic

load_dotenv()

# from models import User

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta
        or timedelta(minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )
    return token


@app.post("/register", response_model=UserPublic)
async def register_user(user: UserCreate):
    # check if user already exists
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    user_in_db = UserInDB(
        email=user.email, hashed_password=hashed, full_name=user.full_name
    )

    await users_collection.insert_one(user_in_db.dict())

    return UserPublic(email=user.email, full_name=user.full_name)


@app.post("/login")
async def login(request: LoginRequest):
    # find user
    user = await users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Convert MongoDB result to UserInDB
    user_in_db = UserInDB(**user)

    # check password
    if not verify_password(request.password, user_in_db.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # create token
    token = create_access_token({"sub": user_in_db.email})

    return {"access_token": token, "token_type": "bearer"}
