import hashlib
import os
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.models.document import Document

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


async def validate_file(file: UploadFile):
    """
    Validate uploaded file type and size.
    """

    # Validate file extension
    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail={
                "errorCode": "INVALID_FILE_TYPE",
                "message": "Only PDF, PNG and JPEG files are supported."
            }
        )

    # Read file content
    content = await file.read()

    # Validate file size
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail={
                "errorCode": "FILE_TOO_LARGE",
                "message": "Uploaded file exceeds the maximum allowed size."
            }
        )

    # Reset file pointer so it can be read again later
    await file.seek(0)

    return True

async def generate_file_hash(file: UploadFile) -> str:
    """
    Generate SHA-256 hash for uploaded file.
    """

    sha256 = hashlib.sha256()

    while chunk := await file.read(4096):
        sha256.update(chunk)

    await file.seek(0)

    return sha256.hexdigest()

async def check_duplicate_document(db: Session, file_hash: str):
    """
    Check if a document with the same SHA-256 hash already exists.
    """

    existing_document = (
        db.query(Document)
        .filter(Document.file_hash == file_hash)
        .first()
    )

    if existing_document:
        raise HTTPException(
            status_code=409,
            detail={
                "errorCode": "DUPLICATE_DOCUMENT",
                "message": "This document has already been processed."
            }
        )