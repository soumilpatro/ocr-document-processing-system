import uuid

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    filename = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    file_hash = Column(String, unique=True, nullable=False)

    status = Column(String, nullable=False, default="UPLOADED")

    pages = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )