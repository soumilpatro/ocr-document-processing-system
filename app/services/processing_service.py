import os
import tempfile
import uuid

from fastapi import UploadFile
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.header import Header
from app.models.transaction import Transaction

from app.services.response_service import build_extracted_fields
from app.services.upload_service import (
    validate_file,
    generate_file_hash,
    check_duplicate_document,
)

from app.services.storage_service import save_uploaded_file

from app.services.pdf_service import extract_text_from_pdf
from app.services.status_service import determine_document_status

from app.services.extraction.document_parser import split_document
from app.services.extraction.header_extractor import extract_header
from app.services.extraction.transaction_extractor import extract_transactions

from app.services.confidence.confidence_service import overall_confidence
from app.services.validation.validation_service import validate_document


async def process_document(
    file: UploadFile,
    db: Session,
):

    # ---------------------------------
    # Validate Upload
    # ---------------------------------

    await validate_file(file)

    file_hash = await generate_file_hash(file)

    await check_duplicate_document(db, file_hash)

    # ---------------------------------
    # Save Uploaded File
    # ---------------------------------

    saved_path = await save_uploaded_file(file)

    # ---------------------------------
    # OCR
    # ---------------------------------

    text = extract_text_from_pdf(saved_path)
    if not text or text.strip() == "":
       raise HTTPException(
        status_code=422,
        detail={
            "errorCode": "NO_TEXT_EXTRACTED",
            "message": "No readable text could be extracted from the uploaded document."
        }
    )

    sections = split_document(text)
    print("\n========== HEADER TEXT ==========\n")
    print(sections["header"])

    header = extract_header(
        sections["header"]
    )

    transactions = extract_transactions(
        sections["transactions"]
    )

    # ---------------------------------
    # Derive Statement Period if Missing
    # ---------------------------------

    if transactions:

       dates = sorted(
           
           txn.date
           for txn in transactions
           if txn.date
       )
        

       if dates:
           
           if header.statement_period.from_date is None:
               header.statement_period.from_date = dates[0]

           if header.statement_period.to_date is None:
               header.statement_period.to_date = dates[-1]
        

        
    confidence = overall_confidence(
        header,
        transactions
    )

    validation = validate_document(
        header,
        transactions
    )

    status = determine_document_status(
    confidence["overall"],
    validation
)

    # ---------------------------------
    # Save Database
    # ---------------------------------

    document_id = str(uuid.uuid4())

    document = Document(
        id=document_id,
        filename=file.filename,
        file_path=saved_path,
        file_hash=file_hash,
        status=status,
        pages=len(text.split("\f"))
    )

    db.add(document)

    header_row = Header(
        id=str(uuid.uuid4()),
        document_id=document_id,
        account_holder=header.account_holder,
        account_number=header.account_number,
        branch=header.branch,
        ifsc=header.ifsc,
        statement_date=header.statement_date,
        statement_from=header.statement_period.from_date,
        statement_to=header.statement_period.to_date
    )

    db.add(header_row)

    for txn in transactions:

        db.add(

            Transaction(

                document_id=document_id,

                date=txn.date,

                description=txn.description,

                debit=txn.debit,

                credit=txn.credit,

                balance=txn.balance

            )

        )

    db.commit()

    return {

    "documentId": document_id,

    "status": status,

    "pages": len(text.split("\f")),

    "confidence": confidence,

    "validation": validation,

    # Assignment Requirement
    "extractedFields": build_extracted_fields(
        header,
        confidence
    ),

    # Existing Response
    "header": header.model_dump(),

    "transactions": [

        txn.model_dump()

        for txn in transactions

    ]

}