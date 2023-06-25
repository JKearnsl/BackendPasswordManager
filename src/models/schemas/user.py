import uuid
from datetime import datetime

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
    hashed_password: str
    public_key: str
    enc_private_key: str

    @validator('username')
    def username_valid(cls, value):
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


class UserSignIn(BaseModel):
    username: str
    hashed_password: str


class UsernameUpdate(BaseModel):
    username: str
    new_hashed_password: str
    old_hashed_password: str

    @validator('username')
    def username_valid(cls, value):
        if not validators.is_valid_username(value):
            raise ValueError("Инвалидный username")
        return value


class UserKeysUpdate(BaseModel):
    public_key: str
    enc_private_key: str
    hashed_password: str

    @validator('public_key')
    def public_key_len(cls, value):
        if not validators.is_base64(value):
            raise ValueError("Инвалидный public_key: не является base64")
        return value

    @validator('enc_private_key')
    def enc_private_key_len(cls, value):
        if not validators.is_base64(value):
            raise ValueError("Инвалидный enc_private_key: не является base64")
        return value


class Keys(BaseModel):
    public_key: str
    enc_private_key: str

    class Config:
        orm_mode = True
