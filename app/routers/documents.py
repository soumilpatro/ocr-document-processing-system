from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.document_service import create_document
from app.services.storage_service import save_uploaded_file
from app.services.upload_service import (
    check_duplicate_document,
    generate_file_hash,
    validate_file,
)

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Step 1: Validate file
    await validate_file(file)

    # Step 2: Generate SHA-256 hash
    file_hash = await generate_file_hash(file)

    # Step 3: Check duplicates
    await check_duplicate_document(db, file_hash)

    # Step 4: Save file locally
    file_path = await save_uploaded_file(file)

    # Step 5: Save metadata in DB
    document = create_document(
        db=db,
        filename=file.filename,
        file_path=file_path,
        file_hash=file_hash,
    )

    return {
        "documentId": document.id,
        "status": document.status,
        "filename": document.filename,
        "filePath": document.file_path,
    }