import os
from datetime import datetime, timedelta
from typing import List

from auth import hash_password, verify_password
from auth_dependencies import get_current_user
from bson import ObjectId
from database import startups_collection, users_collection
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from models import (
    LoginRequest,
    StartUpPitchCard,
    StartUpPitchCreate,
    StartUpPitchPublic,
    StartUpPitchUpdate,
    StoreUserCreate,
    TokenResponse,
    UserCreate,
    UserInDB,
    UserPublic,
)

load_dotenv()
router = APIRouter(prefix="/api")

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


@router.post("/register", response_model=UserPublic)
async def register_user(user: UserCreate):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    user_in_db = StoreUserCreate(
        email=user.email,
        hashed_password=hashed,
        full_name=user.full_name,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    await users_collection.insert_one(user_in_db.model_dump())

    return UserPublic(email=user.email, full_name=user.full_name)


# ------------------------------
# LOGIN
# ------------------------------


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    user = await users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    user["_id"] = str(user["_id"])
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


@router.get("/profile")
async def profile(current_user: UserInDB = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
    }


# ------------------------------
# REFRESH TOKEN
# ------------------------------


@router.post("/refresh")
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


@router.post("/logout")
async def logout():
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("refresh_token", path="/")
    return response


# ------------------------------
# CREATE A STARTUP PITCH
# ------------------------------
@router.post("/startups")
async def create_startup(
    startup: StartUpPitchCreate, current_user: UserInDB = Depends(get_current_user)
):
    user_id = current_user.id
    startup_data = startup.model_dump()
    startup_data.update(
        {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "total_funded": 0,
            "status": "pending",
        }
    )

    result = await startups_collection.insert_one(startup_data)
    print(result)
    return {"id": str(result.inserted_id)}


# ------------------------------
# GET ALL STARTUPS
# ------------------------------


@router.get("/startups", response_model=List[StartUpPitchCard])
async def get_all_startups():
    startups = await startups_collection.find().to_list(100)
    for s in startups:
        s["_id"] = str(s["_id"])  # convert ObjectId → string
        s["user_id"] = str(s["user_id"])  # do same for user_id if needed
    return startups


# ------------------------------
# GET ALL STARTUPS OF A USER
# ------------------------------


@router.get("/users/{user_id}/startups", response_model=List[StartUpPitchCard])
async def get_all_startups_of_user(user_id: str):
    startups = await startups_collection.find({"user_id": user_id}).to_list(100)
    for s in startups:
        # s["id"] = str(s["_id"])
        s["_id"] = str(s["_id"])  # convert ObjectId → string
        s["user_id"] = str(s["user_id"])  # do same for user_id if needed
    return startups


# ------------------------------
# GET A STARTUP PITCH BY ID
# ------------------------------


@router.get(
    "/startups/{startup_id}",
    response_model=StartUpPitchPublic,
    response_model_by_alias=False,
)
async def get_startup(startup_id: str):
    # convert string → ObjectId
    try:
        oid = ObjectId(startup_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid startup ID")

    startup = await startups_collection.find_one({"_id": oid})

    if startup is None:
        raise HTTPException(status_code=404, detail="Startup not found")

    # convert ObjectId → str
    startup["_id"] = str(startup["_id"])
    startup["user_id"] = str(startup["user_id"])

    return startup


# ------------------------------
# UPDATE A PITCH
# ------------------------------


@router.put("/startups/{startup_id}", response_model=StartUpPitchPublic)
async def update_startup(
    startup_id: str,
    startup: StartUpPitchUpdate,
    current_user: UserInDB = Depends(get_current_user),
):
    try:
        oid = ObjectId(startup_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid startup ID")

    # 1) Get existing startup
    existing = await startups_collection.find_one({"_id": oid})
    if existing is None:
        raise HTTPException(status_code=404, detail="Startup not found")

    # 2) Make sure the logged-in user owns this startup
    if str(existing["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not allowed")

    # 3) Get only fields user sent
    update_data = startup.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    # 4) Update DB
    await startups_collection.update_one({"_id": oid}, {"$set": update_data})

    # 5) Fetch updated document
    updated = await startups_collection.find_one({"_id": oid})

    updated["_id"] = str(updated["_id"])
    updated["user_id"] = str(updated["user_id"])

    return updated


# ------------------------------
# DELETE A PITCH
# ------------------------------


@router.delete("/startups/{startup_id}")
async def delete_startup(
    startup_id: str,
    current_user: UserInDB = Depends(get_current_user),
):
    try:
        oid = ObjectId(startup_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid startup ID")

    # 1) Get existing startup
    existing = await startups_collection.find_one({"_id": oid})
    if existing is None:
        raise HTTPException(status_code=404, detail="Startup not found")

    # 2) Make sure the logged-in user owns this startup
    if str(existing["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not allowed")

    # 3) Delete startup
    await startups_collection.delete_one({"_id": oid})

    return {"message": "Startup deleted"}
