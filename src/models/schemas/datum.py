import uuid
from datetime import datetime

from pydantic import BaseModel, validator

from src.utils import validators


class Datum(BaseModel):
    id: uuid.UUID
    username: str | None
    enc_password: str | None

    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class NewDatum(BaseModel):
    username: str | None
    enc_password: str | None

    @validator("username")
    def username_validator(cls, value):
        if value is None:
            return None
        if len(value) > 64:
            raise ValueError("Длина username должна быть не более 64 символов")
        return value

    @validator("enc_password")
    def enc_password_validator(cls, value):
        if value is None:
            return value
        if not validators.is_base64(value):
            raise ValueError("Инвалидный enc_password: не является base64")

        # RSA 2136 bits => 2136 / 8 = 267 bytes len of key
        # Base64 len: 4 * math.ceil(DATA_LEN / 3) => 4 * math.ceil(267 / 3) = 356
        if len(value) != 356:
            raise ValueError("Инвалидный enc_password: не является RSA 2136 bits")
        return value


class UpdateDatum(NewDatum):
    pass
