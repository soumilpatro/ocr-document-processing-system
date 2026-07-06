import re

from app.services.normalization.text_normalizer import normalize_text
from app.services.normalization.date_normalizer import normalize_date
from app.schemas import HeaderSchema, StatementPeriod


ACCOUNT_LABELS = [
    "ACCOUNT NUMBER",
    "ACCOUNT NO",
    "ACCOUNT NO.",
    "A/C NO",
    "A/C NUMBER",
    "ACCOUNT#",
    "ACCOUNT #",
]

NAME_LABELS = [
    "ACCOUNT HOLDER",
    "ACCOUNT NAME",
    "CUSTOMER NAME",
    "NAME",
    "A/C NAME",
]


def is_valid_name(candidate: str) -> bool:

    candidate = candidate.strip()

    if len(candidate) < 3:
        return False

    if len(candidate) > 60:
        return False

    if len(re.findall(r"\d", candidate)) > 2:
        return False

    blacklist = [
        "ACCOUNT",
        "STATEMENT",
        "BRANCH",
        "BALANCE",
        "DATE",
        "IFSC",
        "MICR",
        "EMAIL",
        "PHONE",
        "ADDRESS",
    ]

    upper = candidate.upper()

    if any(word in upper for word in blacklist):
        return False

    return True


def is_valid_account_number(candidate: str) -> bool:

    candidate = candidate.strip()

    if len(candidate) < 4:
        return False

    return bool(re.fullmatch(r"[0-9Xx*\s]+", candidate))


def extract_account_holder(text: str):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    # ---------------------------------
    # Strategy 1
    # Name on same line as label
    # ---------------------------------

    for line in lines:

        upper = line.upper()

        if any(label in upper for label in NAME_LABELS):

            parts = re.split(r":", line, maxsplit=1)

            if len(parts) > 1:

                candidate = parts[1].strip()

                if is_valid_name(candidate):
                    return candidate

    # ---------------------------------
    # Strategy 2
    # Name on next few lines
    # ---------------------------------

    for index, line in enumerate(lines):

        upper = line.upper()

        if any(label in upper for label in NAME_LABELS):

            for offset in range(1, 4):

                if index + offset >= len(lines):
                    break

                candidate = lines[index + offset]

                if is_valid_name(candidate):
                    return candidate

    # ---------------------------------
    # Strategy 3
    # First uppercase-looking name
    # ---------------------------------

    for candidate in lines[:10]:

        if is_valid_name(candidate):

            if candidate.upper() == candidate:
                return candidate.title()

    return None

def extract_account_number(text: str):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    for line in lines:

        upper = line.upper()

        if any(label in upper for label in ACCOUNT_LABELS):

            match = re.search(
                r"([0-9Xx*]{4,})",
                line
            )

            if match:
                return match.group(1)

    # fallback

    for line in lines:

        match = re.search(
            r"\b[0-9]{9,18}\b",
            line
        )

        if match:
            return match.group(0)

    return None


def extract_ifsc(text: str):

    match = re.search(
        r"IFSC\s*[:\-]?\s*([A-Z]{4}0[A-Z0-9]{6})",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).upper()

    return None


def extract_branch(text: str):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    for line in lines:

        if "BRANCH" in line.upper():

            parts = line.split(":")

            if len(parts) > 1:
                return parts[1].strip()

    return None


def extract_statement_date(text: str):

    match = re.search(
        r"STATEMENT DATE\s*[:\-]?\s*([^\n]+)",
        text,
        re.IGNORECASE,
    )

    if match:

        normalized = normalize_date(
            match.group(1).strip()
        )

        return normalized

    return None


def extract_statement_period(text: str):

    date_pattern = (
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        r"|"
        r"\d{1,2}[- ](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[- ]\d{2,4}"
        r"|"
        r"\d{4}[/-]\d{1,2}[/-]\d{1,2}"
    )

    matches = re.findall(
        date_pattern,
        text,
        flags=re.IGNORECASE,
    )

    normalized_dates = []

    for date in matches:

        normalized = normalize_date(date)

        if normalized:
            normalized_dates.append(normalized)

    normalized_dates = list(
        dict.fromkeys(normalized_dates)
    )

    if len(normalized_dates) >= 2:

        return {
            "from": normalized_dates[0],
            "to": normalized_dates[1],
        }

    return {
        "from": None,
        "to": None,
    }


def extract_header(header_text: str) -> HeaderSchema:

    header_text = normalize_text(header_text)

    period = extract_statement_period(header_text)

    return HeaderSchema(

        account_holder=extract_account_holder(
            header_text
        ),

        account_number=extract_account_number(
            header_text
        ),

        branch=extract_branch(
            header_text
        ),

        ifsc=extract_ifsc(
            header_text
        ),

        statement_date=extract_statement_date(
            header_text
        ),

        statement_period=StatementPeriod(
            from_date=period["from"],
            to_date=period["to"],
        ),
    )