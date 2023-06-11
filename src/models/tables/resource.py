import uuid

from sqlalchemy import Column, String, Enum, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.db import Base


class Resource(Base):
    __tablename__ = "resources"
    __table_args__ = {'extend_existing': True}

    id = Column(Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(Text(128), nullable=False)

    owner_id = Column(Text(length=36), ForeignKey("users.id"), nullable=False)
    owner = relationship("models.tables.user.User", back_populates="resources")
    data = relationship("models.tables.datum.Datum", back_populates="resource")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
