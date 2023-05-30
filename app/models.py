import uuid
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class CustomerModel(Base):
    __tablename__ = 'users'
    id = Column(
        'id',
        String(length=36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    name = Column(String,  nullable=False)
    description = Column(String, nullable=False)
