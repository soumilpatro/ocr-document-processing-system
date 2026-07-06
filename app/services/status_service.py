from app.config.settings import settings


def determine_document_status(
    confidence: float,
    validation: dict,
):
    """
    Decide whether a document is OK
    or requires manual review.
    """

    validation_errors = (
        len(validation["header"])
        + len(validation["transactions"])
    )

    # Validation errors always require review
    if validation_errors > 0:
        return "NEEDS_REVIEW"

    # Confidence threshold comes from .env
    if confidence < settings.OCR_CONFIDENCE_THRESHOLD:
        return "NEEDS_REVIEW"

    return "OK"