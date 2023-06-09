import uuid

from sqlalchemy import Column, String, Enum, DateTime, func, Text
from sqlalchemy.orm import relationship

# from sqlalchemy import UUID  # Only for psql

from src.db import Base

from src.models.enums.role import UserRole


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)

    resources = relationship("models.tables.resource.Resource", back_populates="owner")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
