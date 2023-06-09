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
