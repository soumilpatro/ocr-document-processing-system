import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Header(Base):
    __tablename__ = "headers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    document_id = Column(
        String,
        ForeignKey("documents.id"),
        nullable=False,
        unique=True,
    )

    account_holder = Column(String)
    account_number = Column(String)
    branch = Column(String)
    ifsc = Column(String)
    statement_date = Column(String)
    statement_from = Column(String)
    statement_to = Column(String)

    document = relationship("Document", back_populates="header")