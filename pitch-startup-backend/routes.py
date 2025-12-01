import os
import re
from datetime import datetime, timedelta
from typing import List

from auth import hash_password, verify_password
from auth_dependencies import get_current_user
from bson import ObjectId
from database import investments_collection, startups_collection, users_collection
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi._compat.v1 import RequestErrorModel
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from models import (
    InvestementInDB,
    InvestmentRequest,
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


# ------------------------------
# ENHANCED USER PROFILE (Single Call)
# ------------------------------


@router.get("/users/{user_id}/profile")
async def get_user_full_profile(user_id: str):
    """Get complete user profile with startups and investments in ONE call"""

    # 1. Get user basic info
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Get user's startups
    startups = await startups_collection.find({"user_id": user_id}).to_list(None)
    for s in startups:
        s["_id"] = str(s["_id"])
        s["user_id"] = str(s["user_id"])

    # 3. Get user's investments
    investments = await investments_collection.find({"user_id": user_id}).to_list(None)
    for inv in investments:
        inv["_id"] = str(inv["_id"])
        inv["user_id"] = str(inv["user_id"])
        inv["startup_id"] = str(inv["startup_id"])

    # 4. Calculate totals
    total_raised = sum(s.get("total_funded", 0) for s in startups)
    total_invested = sum(inv.get("amount", 0) for inv in investments)

    return {
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "full_name": user["full_name"],
            "created_at": user.get("created_at"),
        },
        "startups": startups,
        "investments": investments,
        "stats": {
            "total_startups": len(startups),
            "total_raised": total_raised,
            "total_invested": total_invested,
            "total_investments": len(investments),
        },
    }


# ------------------------------
# DASHBOARD (For Current Logged-in User)
# ------------------------------


@router.get("/dashboard")
async def get_dashboard(current_user: UserInDB = Depends(get_current_user)):
    """Get complete dashboard for logged-in user"""

    user_id = current_user.id

    # Get user's startups
    startups = await startups_collection.find({"user_id": user_id}).to_list(None)
    for s in startups:
        s["_id"] = str(s["_id"])
        s["user_id"] = str(s["user_id"])

    # Get user's investments
    investments = await investments_collection.find({"user_id": user_id}).to_list(None)
    for inv in investments:
        inv["_id"] = str(inv["_id"])
        inv["user_id"] = str(inv["user_id"])
        inv["startup_id"] = str(inv["startup_id"])

    # Calculate totals
    total_raised = sum(s.get("total_funded", 0) for s in startups)
    total_invested = sum(inv.get("amount", 0) for inv in investments)

    return {
        "my_startups": startups,
        "my_investments": investments,
        "total_raised": total_raised,
        "total_invested": total_invested,
        "stats": {
            "startups_count": len(startups),
            "investments_count": len(investments),
        },
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


# ------------------------------
# INVEST IN A PITCH
# ------------------------------
#
@router.post("/startups/{startup_id}/invest")
async def invest(
    startup_id: str,
    data: InvestmentRequest,
    current_user: UserInDB = Depends(get_current_user),
):
    amount = data.amount
    user_id = current_user.id
    invested_at = datetime.utcnow()

    investment_doc = {
        "user_id": user_id,
        "startup_id": startup_id,
        "amount": amount,
        "invested_at": invested_at,
    }

    result = await investments_collection.insert_one(investment_doc)
    if result.inserted_id:
        await startups_collection.update_one(
            {"_id": ObjectId(startup_id)}, {"$inc": {"total_funded": amount}}
        )

        # Convert Mongo ObjectIds → strings
    investment_doc["_id"] = str(investment_doc["_id"])
    investment_doc["user_id"] = str(investment_doc["user_id"])
    investment_doc["startup_id"] = str(investment_doc["startup_id"])

    return InvestementInDB(**investment_doc)


# ------------------------------
# SEE ALL INVESTMENT HISTORY OF THE USER
# ------------------------------


@router.get("/users/{user_id}/investments")
async def get_user_investments(user_id: str):
    """Get investments of any user by their ID"""

    investments = await investments_collection.find({"user_id": user_id}).to_list(None)

    for investment in investments:
        investment["_id"] = str(investment["_id"])
        investment["user_id"] = str(investment["user_id"])
        investment["startup_id"] = str(investment["startup_id"])

    return investments


# ------------------------------
# GET INVESTMENTS FOR A STARTUP
# ------------------------------


@router.get("/startups/{startup_id}/investments")
async def get_startup_investments(startup_id: str):
    """Get all investments made to a specific startup"""

    try:
        ObjectId(startup_id)  # Validate
    except:
        raise HTTPException(status_code=400, detail="Invalid startup ID")

    investments = await investments_collection.find({"startup_id": startup_id}).to_list(
        None
    )

    for inv in investments:
        inv["_id"] = str(inv["_id"])
        inv["user_id"] = str(inv["user_id"])
        inv["startup_id"] = str(inv["startup_id"])

    return investments


# ------------------------------
# GET STARTUP ANALYTICS
# ------------------------------


@router.get("/startups/{startup_id}/analytics")
async def get_startup_analytics(startup_id: str):
    """Get detailed analytics for a startup"""

    try:
        oid = ObjectId(startup_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid startup ID")

    # Get startup
    startup = await startups_collection.find_one({"_id": oid})
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    # Get all investments
    investments = await investments_collection.find({"startup_id": startup_id}).to_list(
        None
    )

    # Calculate analytics
    total_funded = startup.get("total_funded", 0)
    funding_goal = startup.get("funding_goal", 0)
    investor_count = len(investments)
    funding_progress = (total_funded / funding_goal * 100) if funding_goal > 0 else 0

    # Recent investments (last 5)
    recent_investments = sorted(
        investments, key=lambda x: x.get("invested_at", datetime.utcnow()), reverse=True
    )[:5]

    for inv in recent_investments:
        inv["_id"] = str(inv["_id"])
        inv["user_id"] = str(inv["user_id"])
        inv["startup_id"] = str(inv["startup_id"])

    return {
        "startup_id": startup_id,
        "total_funded": total_funded,
        "funding_goal": funding_goal,
        "investor_count": investor_count,
        "funding_progress": round(funding_progress, 2),
        "recent_investments": recent_investments,
    }


# ------------------------------
# SEARCH AND FILTER STARTUPS
# ------------------------------


@router.get("/search")
async def search_startups(
    q: str | None = None,
    category: str | None = None,
):
    query = {}

    # 🔍 Search (title, description, pitch)
    if q:
        query["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"pitch": {"$regex": q, "$options": "i"}},
        ]

    # 🏷 Category filter
    if category:
        query["category"] = category

    startups = await startups_collection.find(query).limit(50).to_list(50)

    for s in startups:
        s["_id"] = str(s["_id"])
        s["user_id"] = str(s["user_id"])

    return startups


@router.get("/startups/trending")
async def get_trending_startups():
    pipeline = [
        {"$sort": {"timestamp": -1}},  # latest investments first
        {"$group": {"_id": "$startup_id"}},  # unique startups
        {"$limit": 10},
    ]

    recent = await investments_collection.aggregate(pipeline).to_list(10)
    ids = [r["_id"] for r in recent]

    startups = await startups_collection.find({"_id": {"$in": ids}}).to_list(10)

    for s in startups:
        s["_id"] = str(s["_id"])
        s["user_id"] = str(s["user_id"])

    return startups


@router.get("/startups/top-funded")
async def get_top_funded_startups(limit: int = 10):
    startups = (
        await startups_collection.find({})
        .sort("total_funded", -1)
        .limit(limit)
        .to_list(limit)
    )

    for s in startups:
        s["_id"] = str(s["_id"])
        s["user_id"] = str(s["user_id"])

    return startups


@router.get("/categories")
async def get_categories():
    pipeline = [{"$group": {"_id": "$category"}}, {"$sort": {"_id": 1}}]

    items = await startups_collection.aggregate(pipeline).to_list(None)
    categories = [item["_id"] for item in items if item["_id"]]

    return {"categories": categories}
