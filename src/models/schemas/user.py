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
    public_key: str
    enc_private_key: str

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

    @validator('public_key')
    def public_key_len(cls, value):
        if value is None:
            return None
        if not validators.is_base64(value):
            raise ValueError("Инвалидный public_key: не является base64")
        return value

    @validator('enc_private_key')
    def enc_private_key_len(cls, value):
        if value is None:
            return None
        if not validators.is_base64(value):
            raise ValueError("Инвалидный enc_private_key: не является base64")
        return value


class UserSignIn(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str | None
    public_key: str | None
    enc_private_key: str | None

    @validator('username')
    def username_len(cls, value):
        if value is None:
            return None
        if not validators.is_valid_username(value):
            raise ValueError("Инвалидный username")
        return value

    @validator('public_key')
    def public_key_len(cls, value):
        if value is None:
            return None
        if not validators.is_base64(value):
            raise ValueError("Инвалидный public_key: не является base64")
        return value

    @validator('enc_private_key')
    def enc_private_key_len(cls, value):
        if value is None:
            return None
        if not validators.is_base64(value):
            raise ValueError("Инвалидный enc_private_key: не является base64")
        return value


class Keys(BaseModel):
    public_key: str
    enc_private_key: str

    class Config:
        orm_mode = True
