import uuid
from datetime import datetime

from pydantic import BaseModel, validator


class Datum(BaseModel):
    id: uuid.UUID
    username: str | None
    password: str | None

    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class NewDatum(BaseModel):
    username: str | None
    password: str | None

    @validator("password")
    def password_validator(cls, value):
        if value is None:
            return None
        if len(value) > 64:
            raise ValueError("Длина пароля должна быть не более 64 символов")
        return value

    @validator("username")
    def username_validator(cls, value):
        if value is None:
            return None
        if len(value) > 64:
            raise ValueError("Длина username должна быть не более 64 символов")
        return value
