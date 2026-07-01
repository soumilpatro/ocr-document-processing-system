import re


def extract_name(text: str):
    """
    Extract a person's name from OCR text.
    """

    patterns = [
        r"Name[:\s]+([A-Za-z ]+)",
        r"Customer Name[:\s]+([A-Za-z ]+)",
        r"Applicant[:\s]+([A-Za-z ]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


def extract_date(text: str):
    """
    Extract date in DD/MM/YYYY format.
    """

    match = re.search(
        r"\b\d{2}/\d{2}/\d{4}\b",
        text
    )

    if match:
        return match.group()

    return None


def extract_amount(text: str):
    """
    Extract monetary amount.
    """

    match = re.search(
        r"\b\d+(?:,\d{3})*(?:\.\d{2})?\b",
        text
    )

    if match:
        return match.group()

    return None


def extract_id_number(text: str):
    """
    Extract ID numbers like:
    ABC12345
    AB123456
    ID12345678
    """

    patterns = [
        r"\b[A-Z]{2,5}\d{4,10}\b",
        r"\bID\d{4,10}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return match.group()

    return None


def extract_fields(text: str):
    """
    Extract all supported fields.
    """

    return {
        "name": extract_name(text),
        "date": extract_date(text),
        "amount": extract_amount(text),
        "id_number": extract_id_number(text),
    }