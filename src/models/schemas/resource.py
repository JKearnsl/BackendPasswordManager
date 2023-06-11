import uuid
from datetime import datetime

from pydantic import BaseModel, validator


class Resource(BaseModel):
    id: uuid.UUID
    title: str

    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class NewResource(BaseModel):
    title: str

    @validator('title')
    def title_must_be_unique(cls, v):
        if len(v) > 128:
            raise ValueError('Title должен быть не более 128 символов')
        return v
