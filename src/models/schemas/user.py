import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from src.models.enums.role import UserRole
from src.utils import validators


class User(BaseModel):
    id: uuid.UUID
    username: str
    role: UserRole
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class UserSignUp(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_len(cls, value):
        if not validators.is_valid_username(value):
            raise ValueError("Инвалидный username")
        return value

    @validator('password')
    def password_must_be_valid(cls, value):
        if not validators.is_valid_password(value):
            raise ValueError("Слабый или инвалидный пароль")
        return value


class UserSignIn(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]

    @validator('username')
    def username_len(cls, value):
        if not validators.is_valid_username(value):
            raise ValueError("Инвалидный username")
        return value
