from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field, condate
from src.database.models import Role


class UserModel(BaseModel):
    first_name: str | None = Field(default="", max_length=25)
    last_name: str | None = Field(default="", max_length=30)
    username: str = Field(min_length=6, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)
    phone_number: str | None = Field(default="", max_length=25)
    born_date: date | None
    description: str | None = Field(default="", max_length=250)


class UserDb(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    username: str
    email: EmailStr
    phone_number: str | None
    born_date: date | None
    description: str | None
    avatar: str
    roles: Role
    confirmed: bool | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class UserEmailModel(BaseModel):
    email: EmailStr


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
