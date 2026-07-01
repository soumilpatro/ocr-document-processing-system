from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    filename: str,
    file_path: str,
    file_hash: str,
):
    """
    Save uploaded document metadata in the database.
    """

    document = Document(
        filename=filename,
        file_path=file_path,
        file_hash=file_hash,
        status="UPLOADED",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document