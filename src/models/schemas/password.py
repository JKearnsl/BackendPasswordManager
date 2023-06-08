import uuid

from pydantic import BaseModel, validator


class Password(BaseModel):
    id: uuid.UUID
    username: str | None
    password: str | None

    class Config:
        orm_mode = True


class NewPassword(BaseModel):
    username: str | None
    password: str | None
