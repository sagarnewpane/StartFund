import os

from database import users_collection
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# or import from where you defined it
from models import UserInDB

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # find user in DB
    user = await users_collection.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])
    user = UserInDB(**user)
    return user
