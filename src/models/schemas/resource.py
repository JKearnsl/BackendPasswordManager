import uuid
from datetime import datetime

from pydantic import BaseModel


class Resource(BaseModel):
    id: uuid.UUID
    title: str

    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class NewResource(BaseModel):
    title: str
