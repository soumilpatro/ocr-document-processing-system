from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.document import Document
from app.models.header import Header
from app.models.transaction import Transaction

from app.schemas.header_schema import HeaderSchema, StatementPeriod
from app.schemas.transaction_schema import TransactionSchema

from app.services.validation.validation_service import validate_document
from app.services.confidence.confidence_service import overall_confidence

router = APIRouter(
    prefix="/api/documents",
    tags=["Validation"]
)


@router.post("/{document_id}/validate")
def validate_saved_document(
    document_id: str,
    db: Session = Depends(get_db)
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

    transactions = []

    for txn in transactions_db:

        transactions.append(

            TransactionSchema(
                date=txn.date,
                description=txn.description,
                debit=txn.debit,
                credit=txn.credit,
                balance=txn.balance,
            )

        )

    confidence = overall_confidence(
        header,
        transactions
    )

    validation= validate_document(
        header,
        transactions
    )
    return {
        "documentId": document.id,
        "status": document.status,
        "confidence": confidence,
        "validation": validation
    }
    