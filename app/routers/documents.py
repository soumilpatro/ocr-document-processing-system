from fastapi import APIRouter, Depends, File, UploadFile, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.document import Document

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


# -------------------------------------------------------
# Upload Document
# -------------------------------------------------------
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

    # Step 5: Save metadata
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


# -------------------------------------------------------
# Get All Documents
# -------------------------------------------------------
@router.get("")
def get_all_documents(
    db: Session = Depends(get_db),
):

    documents = db.query(Document).all()

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "status": doc.status,
            "pages": doc.pages,
            "created_at": doc.created_at,
            "updated_at": doc.updated_at,
        }
        for doc in documents
    ]
# -------------------------------------------------------
# Search Documents
# -------------------------------------------------------
@router.get("/search")
def search_documents(
    filename: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
):

    query = db.query(Document)

    if filename:
        query = query.filter(
            Document.filename.ilike(f"%{filename}%")
        )

    if status:
        query = query.filter(
            Document.status == status
        )

    documents = query.all()

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "status": doc.status,
            "pages": doc.pages,
            "created_at": doc.created_at,
        }
        for doc in documents
    ]
# -------------------------------------------------------
# Get Single Document
# -------------------------------------------------------
@router.get("/{document_id}")
def get_document(
    document_id: str,
    db: Session = Depends(get_db),
):

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        return {
            "error": "Document not found"
        }

    return {
        "id": document.id,
        "filename": document.filename,
        "status": document.status,
        "filePath": document.file_path,
        "pages": document.pages,
        "created_at": document.created_at,
        "updated_at": document.updated_at,
    }

