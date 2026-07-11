import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.header import Header
from app.models.transaction import Transaction

from app.services.confidence.confidence_service import overall_confidence
from app.services.status_service import determine_document_status
from app.services.validation.validation_service import validate_document
from app.services.response_service import build_extracted_fields

from app.services.masking_service import (
    mask_name,
    mask_account_number,
    mask_ifsc,
)


def process_manual_document(data, db: Session):

    confidence = overall_confidence(
        data,
        data.transactions
    )

    validation = validate_document(
        data,
        data.transactions
    )

    status = determine_document_status(
        confidence["overall"],
        validation
    )

    document_id = str(uuid.uuid4())

    document = Document(

        id=document_id,

        filename="MANUAL_ENTRY",

        file_path="MANUAL",

        file_hash=str(uuid.uuid4()),

        status=status,

        pages=0,

    )

    db.add(document)

    header = Header(

        id=str(uuid.uuid4()),

        document_id=document_id,

        account_holder=data.account_holder,

        account_number=data.account_number,

        branch=data.branch,

        ifsc=data.ifsc,

        statement_date=data.statement_date,

        statement_from=data.statement_period.from_date,
        statement_to=data.statement_period.to_date,

    )

    db.add(header)

    for txn in data.transactions:

        db.add(

            Transaction(

                document_id=document_id,

                date=txn.date,

                description=txn.description,

                debit=txn.debit,

                credit=txn.credit,

                balance=txn.balance,

            )

        )

    db.commit()

    return {

        "documentId": document_id,

        "status": status,

        "confidence": confidence,

        "validation": validation,

        "extractedFields": build_extracted_fields(
            data,
            confidence
        ),

        "header": {

            "account_holder": mask_name(
                data.account_holder
            ),

            "account_number": mask_account_number(
                data.account_number
            ),

            "branch": data.branch,

            "ifsc": mask_ifsc(
                data.ifsc
            ),

            "statement_date": data.statement_date,

            "statement_period": {
                "from_date": data.statement_period.from_date,
                "to_date": data.statement_period.to_date,   

}

        },

        "transactions": [

            txn.model_dump()

            for txn in data.transactions

        ]

    }