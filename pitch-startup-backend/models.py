from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str | None = None
    full_name: str | None = None
    password: str


class UserInDB(BaseModel):
    email: str | None = None
    full_name: str | None = None
    hashed_password: str


class UserPublic(BaseModel):
    email: str | None = None
    full_name: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str
