import os
from datetime import datetime, timedelta

from auth import hash_password, verify_password
from auth_dependencies import get_current_user
from database import users_collection
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from models import LoginRequest, TokenResponse, UserCreate, UserInDB, UserPublic

load_dotenv()

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


# ------------------------------
# TOKEN HELPERS
# ------------------------------


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ------------------------------
# REGISTER
# ------------------------------


@app.post("/register", response_model=UserPublic)
async def register_user(user: UserCreate):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    user_in_db = UserInDB(
        email=user.email, hashed_password=hashed, full_name=user.full_name
    )

    await users_collection.insert_one(user_in_db.model_dump())

    return UserPublic(email=user.email, full_name=user.full_name)


# ------------------------------
# LOGIN
# ------------------------------


@app.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    user = await users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    user_in_db = UserInDB(**user)

    if not verify_password(request.password, user_in_db.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token({"sub": user_in_db.email})
    refresh_token = create_refresh_token({"sub": user_in_db.email})

    response_data = TokenResponse(access_token=access_token, token_type="bearer")
    response = JSONResponse(content=response_data.model_dump())

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # True in production
        samesite="strict",
        path="/",
    )

    return response


# ------------------------------
# PROTECTED ROUTE
# ------------------------------


@app.get("/profile")
async def profile(current_user: UserInDB = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "full_name": current_user.full_name,
    }


# ------------------------------
# REFRESH TOKEN
# ------------------------------


@app.post("/refresh")
async def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    new_access_token = create_access_token({"sub": username})

    return {"access_token": new_access_token, "token_type": "bearer"}


# ------------------------------
# LOGOUT
# ------------------------------


@app.post("/logout")
async def logout():
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("refresh_token", path="/")
    return response
