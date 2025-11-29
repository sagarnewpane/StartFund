import datetime
from typing import Optional

from motor.docstrings import create_data_key_doc
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pydantic.types import Base64Bytes


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=6)

    @field_validator("password")
    def password_must_contain_number(cls, v):
        if not any(ch.isdigit() for ch in v):
            raise ValueError("Password must contain at least one number")
        return v


class StoreUserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=30)
    hashed_password: str = Field(..., min_length=6)
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserInDB(StoreUserCreate):
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True


class UserPublic(BaseModel):
    email: str | None = None
    full_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Startup Model


class StartUpPitchBase(BaseModel):
    title: str
    description: str
    category: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    pitch: str
    funding_goal: float


class StartUpPitchCreate(StartUpPitchBase):
    pass


class StartUpPitchInDB(StartUpPitchBase):
    id: str = Field(alias="_id")
    user_id: str
    total_funded: float = 0
    status: str = "pending"
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class StartUpPitchPublic(StartUpPitchBase):
    id: str = Field(alias="_id")
    user_id: str
    total_funded: float
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class StartUpPitchCard(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    title: str
    description: str
    category: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    funding_goal: float
    total_funded: float
    status: str
    created_at: datetime.datetime
