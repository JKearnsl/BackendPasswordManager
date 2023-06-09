import uuid

from pydantic import BaseModel, validator


class Datum(BaseModel):
    id: uuid.UUID
    username: str | None
    password: str | None

    class Config:
        orm_mode = True


class NewDatum(BaseModel):
    username: str | None
    password: str | None
