import uuid

from sqlalchemy import Column, String, Enum, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.db import Base


class Datum(Base):
    __tablename__ = "data"
    __table_args__ = {'extend_existing': True}

    id = Column(Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)

    resource_id = Column(Text(length=36), ForeignKey("resources.id"), nullable=True)
    resource = relationship("models.tables.resource.Resource", back_populates="data")

    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
