from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, Query, HTTPException
from sqlalchemy.orm import Session


from app.database.database import get_db

from app.models.document import Document
from app.models.header import Header
from app.models.transaction import Transaction

from app.schemas.header_schema import HeaderSchema, StatementPeriod
from app.schemas.transaction_schema import TransactionSchema
from app.schemas.manual_entry_schema import ManualEntrySchema

from app.services.csv_service import parse_csv
from app.services.bulk_upload_service import process_bulk_documents
from app.services.manual_service import process_manual_document
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
@router.post(
    "/upload",
    summary="Upload Document",
    description="Upload and process a single PDF or image document.",
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return await process_document(file, db)


# -------------------------------------------------------
# Bulk Upload
# -------------------------------------------------------
@router.post(
    "/upload-bulk",
    summary="Upload Multiple Documents",
    description="Upload and process multiple PDF or image documents in one request.",
)
async def upload_bulk_documents(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    return await process_bulk_documents(files, db)

# -------------------------------------------------------
# Manual Entry
# -------------------------------------------------------
@router.post(
    "/manual",
    summary="Manual Document Entry",
    description="Create a document by manually entering header and transaction details.",
    responses={
        200: {
            "description": "Manual document saved successfully."
        },
        400: {
            "description": "Invalid input."
        },
        500: {
            "description": "Internal Server Error."
        },
    },
)
def manual_document_entry(
    data: ManualEntrySchema,
    db: Session = Depends(get_db),
):
    return process_manual_document(
        data,
        db,
    )


# -------------------------------------------------------
# CSV Upload
# -------------------------------------------------------
@router.post(
    "/upload/csv",
    summary="Upload CSV",
    description="Bulk import bank statements from a CSV file.",
    responses={
        200: {
            "description": "CSV uploaded successfully."
        },
        400: {
            "description": "Invalid CSV file."
        },
        500: {
            "description": "Internal Server Error."
        },
    },
)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    # Validate extension
    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(

            status_code=400,

            detail={

                "errorCode": "INVALID_FILE_TYPE",

                "message": "Only CSV files are supported."

            }

        )

    try:

        contents = await file.read()

        csv_text = contents.decode("utf-8")

        documents = parse_csv(csv_text)

        results = []

        failed = 0

        for document in documents:

            try:

                result = process_manual_document(
                    document,
                    db
                )

                results.append(result)

            except Exception:

                failed += 1

        return {

            "processed": len(results),

            "failed": failed,

            "documents": results

        }

    except Exception:

        raise HTTPException(

            status_code=400,

            detail={

                "errorCode": "INVALID_CSV",

                "message": "Unable to read or parse CSV file."

            }

        )
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
    account_holder: str | None = Query(default=None),
    account_number: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    ifsc: str | None = Query(default=None),
    db: Session = Depends(get_db),
):

    try:

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

        results = [

            {
                "id": doc.id,
                "filename": doc.filename,
                "status": doc.status,
                "pages": doc.pages,
                "created_at": doc.created_at,
            }

            for doc in documents

        ]

        if not results:

            return {

                "count": 0,

                "documents": [],

                "message": "No matching documents found."

            }

        return {

            "count": len(results),

            "documents": results

        }

    except Exception:

        raise HTTPException(

            status_code=500,

            detail={

                "errorCode": "SEARCH_FAILED",

                "message": "Unable to search documents."

            }

        )


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