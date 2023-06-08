import uuid

from pydantic import BaseModel, validator


class Resource(BaseModel):
    id: uuid.UUID
    title: str

    class Config:
        orm_mode = True


class NewResource(BaseModel):
    title: str
