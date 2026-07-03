import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    document_id = Column(
        String,
        ForeignKey("documents.id"),
        nullable=False,
    )

    date = Column(String)
    description = Column(String)
    debit = Column(Float)
    credit = Column(Float)
    balance = Column(Float)

    document = relationship("Document", back_populates="transactions")