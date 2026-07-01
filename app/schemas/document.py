from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    file_path: str
    status: str
    pages: int
    created_at: datetime

    class Config:
        from_attributes = True