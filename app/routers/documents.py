from fastapi import APIRouter, Depends, File, UploadFile, Query, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.document import Document
from app.models.header import Header
from app.models.transaction import Transaction

from app.schemas.header_schema import HeaderSchema, StatementPeriod
from app.schemas.transaction_schema import TransactionSchema

from app.services.processing_service import process_document
from app.services.confidence.confidence_service import overall_confidence
from app.services.validation.validation_service import validate_document

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
    return await process_document(file, db)


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
# -------------------------------------------------------
# Search Documents
# -------------------------------------------------------
@router.get("/search")
def search_documents(
    filename: str | None = Query(default=None),
    status: str | None = Query(default=None),
    account_holder: str | None = Query(default=None),
    account_number: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    ifsc: str | None = Query(default=None),
    db: Session = Depends(get_db),
):

    query = (
        db.query(Document)
        .outerjoin(
            Header,
            Document.id == Header.document_id
        )
    )

    if filename:
        query = query.filter(
            Document.filename.ilike(f"%{filename}%")
        )

    if status:
        query = query.filter(
            Document.status == status
        )

    if account_holder:
        query = query.filter(
            Header.account_holder.ilike(
                f"%{account_holder}%"
            )
        )

    if account_number:
        query = query.filter(
            Header.account_number.ilike(
                f"%{account_number}%"
            )
        )

    if branch:
        query = query.filter(
            Header.branch.ilike(
                f"%{branch}%"
            )
        )

    if ifsc:
        query = query.filter(
            Header.ifsc.ilike(
                f"%{ifsc}%"
            )
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
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    header_db = (
        db.query(Header)
        .filter(Header.document_id == document_id)
        .first()
    )

    transactions_db = (
        db.query(Transaction)
        .filter(Transaction.document_id == document_id)
        .all()
    )

    header = HeaderSchema(

        account_holder=header_db.account_holder,
        account_number=header_db.account_number,
        branch=header_db.branch,
        ifsc=header_db.ifsc,
        statement_date=header_db.statement_date,

        statement_period=StatementPeriod(

            from_date=header_db.statement_from,
            to_date=header_db.statement_to,

        )

    )

    transactions = [

        TransactionSchema(

            date=txn.date,
            description=txn.description,
            debit=txn.debit,
            credit=txn.credit,
            balance=txn.balance,

        )

        for txn in transactions_db

    ]

    confidence = overall_confidence(
        header,
        transactions
    )

    validation = validate_document(
        header,
        transactions
    )

    return {

        "documentId": document.id,
        "filename": document.filename,
        "status": document.status,
        "pages": document.pages,
        "created_at": document.created_at,
        "updated_at": document.updated_at,

        "header": header.model_dump(),

        "transactions": [

            txn.model_dump()

            for txn in transactions

        ],

        "confidence": confidence,

        "validation": validation,

    }