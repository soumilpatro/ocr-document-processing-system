from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import List

from app.services.processing_service import process_document


async def process_bulk_documents(
    files: list[UploadFile],
    db: Session,
):
    """
    Process multiple uploaded documents.
    Each document is processed independently.
    """

    results = []

    processed = 0
    failed = 0

    for file in files:

        try:

            response = await process_document(
                file,
                db,
            )

            processed += 1

            results.append(
                {
                    "filename": file.filename,
                    "status": "SUCCESS",
                    "documentId": response["documentId"],
                }
            )

        except Exception as e:

            failed += 1

            results.append(
                {
                    "filename": file.filename,
                    "status": "FAILED",
                    "message": str(e),
                }
            )

    return {

        "totalFiles": len(files),

        "processed": processed,

        "failed": failed,

        "results": results,

    }