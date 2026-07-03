from fastapi import FastAPI, UploadFile, File
import tempfile
import os
import uuid

from app.database.database import Base, engine, SessionLocal
from app.models import *
from app.models.document import Document
from app.models.header import Header
from app.models.transaction import Transaction

# Import the Documents Router
from app.routers.documents import router as document_router

from app.services.pdf_service import extract_text_from_pdf

from app.services.extraction.document_parser import split_document
from app.services.extraction.header_extractor import extract_header
from app.services.extraction.transaction_extractor import extract_transactions

from app.services.confidence.confidence_service import overall_confidence
from app.services.validation.validation_service import validate_document


# Create all database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="OCR Document Processing System",
    version="1.0.0"
)

# Register Routers
app.include_router(document_router)


@app.get("/")
def home():

    return {
        "message": "OCR Document Processing System"
    }


@app.post("/process")
async def process_document(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp:

        temp.write(await file.read())
        pdf_path = temp.name

    try:

        text = extract_text_from_pdf(pdf_path)

        sections = split_document(text)

        header = extract_header(
            sections["header"]
        )

        transactions = extract_transactions(
            sections["transactions"]
        )

        confidence = overall_confidence(
            header,
            transactions
        )

        validation = validate_document(
            header,
            transactions
        )

        # -----------------------------------------
        # Save to Database
        # -----------------------------------------

        db = SessionLocal()

        document_id = str(uuid.uuid4())

        document = Document(
            id=document_id,
            filename=file.filename,
            file_path=pdf_path,
            file_hash="TEMP_HASH",
            status="PROCESSED",
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
        db.close()

        return {

            "header": header.model_dump(),

            "transactions": [
                txn.model_dump()
                for txn in transactions
            ],

            "confidence": confidence,

            "validation": validation

        }

    finally:

        if os.path.exists(pdf_path):

            os.remove(pdf_path)