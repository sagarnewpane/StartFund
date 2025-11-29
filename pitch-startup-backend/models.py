from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=6)

    @field_validator("password")
    def password_must_contain_number(cls, v):
        if not any(ch.isdigit() for ch in v):
            raise ValueError("Password must contain at least one number")
        return v


class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    full_name: str


class UserPublic(BaseModel):
    email: str | None = None
    full_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
