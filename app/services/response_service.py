from app.config.settings import settings


def field_status(confidence: float) -> str:
    """
    Determine whether a field needs manual review.
    """
    threshold = settings.OCR_CONFIDENCE_THRESHOLD / 100

    if confidence >= threshold:
        return "OK"

    return "NEEDS_REVIEW"


def build_extracted_fields(header, confidence):
    """
    Build assignment-compliant extracted field response.
    """

    header_conf = confidence["header"]

    return {

        "account_holder": {
            "value": header.account_holder,
            "confidence": header_conf["account_holder"],
            "status": field_status(header_conf["account_holder"])
        },

        "account_number": {
            "value": header.account_number,
            "confidence": header_conf["account_number"],
            "status": field_status(header_conf["account_number"])
        },

        "branch": {
            "value": header.branch,
            "confidence": header_conf["branch"],
            "status": field_status(header_conf["branch"])
        },

        "ifsc": {
            "value": header.ifsc,
            "confidence": header_conf["ifsc"],
            "status": field_status(header_conf["ifsc"])
        },

        "statement_date": {
            "value": header.statement_date,
            "confidence": header_conf["statement_date"],
            "status": field_status(header_conf["statement_date"])
        },

        "statement_from": {
            "value": header.statement_period.from_date,
            "confidence": header_conf["statement_period"]["from_date"],
            "status": field_status(
                header_conf["statement_period"]["from_date"]
            )
        },

        "statement_to": {
            "value": header.statement_period.to_date,
            "confidence": header_conf["statement_period"]["to_date"],
            "status": field_status(
                header_conf["statement_period"]["to_date"]
            )
        }

    }