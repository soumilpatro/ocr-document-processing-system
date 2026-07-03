import re

from app.schemas import TransactionSchema
from app.services.normalization.date_normalizer import normalize_date
from app.services.normalization.amount_normalizer import normalize_amount


DATE_PATTERN = (
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|"
    r"\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{2,4}"
)

AMOUNT_PATTERN = r"-?\d[\d,]*\.\d{2}"

HEADER_PATTERNS = [
    "DATE DESCRIPTION",
    "DATE VALUE",
    "CHEQUE",
    "BALANCE",
    "PAGE ",
    "MR ",
]


def is_page_header(line: str) -> bool:

    upper = line.upper().strip()

    for header in HEADER_PATTERNS:
        if header in upper:
            return True

    if upper.startswith("TOTAL "):
        return True

    if upper.startswith("REWARD POINTS"):
        return True

    if upper.startswith("SCHEME "):
        return True

    return False


def clean_lines(text: str):

    cleaned = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        if is_page_header(line):
            continue

        cleaned.append(line)

    return cleaned


def is_date_line(line: str):

    return re.match(
        DATE_PATTERN,
        line,
        flags=re.IGNORECASE,
    ) is not None


def extract_date(line: str):

    match = re.search(
        DATE_PATTERN,
        line,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    return normalize_date(match.group())


def ends_with_amounts(line: str):

    amounts = re.findall(
        AMOUNT_PATTERN,
        line,
    )

    return len(amounts) >= 2


def extract_amounts(line: str):

    amounts = re.findall(
        AMOUNT_PATTERN,
        line,
    )

    values = []

    for amount in amounts:

        value = normalize_amount(amount)

        if value is not None:
            values.append(value)

    return values


def classify_transaction(description, previous_balance, current_balance):

    if (
        previous_balance is not None
        and current_balance is not None
    ):

        if current_balance > previous_balance:
            return "credit"

        if current_balance < previous_balance:
            return "debit"

    text = description.upper()

    credit_keywords = [
        "CRADJ",
        "INTEREST",
        "SALARY",
        "REFUND",
        "DEPOSIT",
        "CREDIT",
        "NEFT",
    ]

    for keyword in credit_keywords:
        if keyword in text:
            return "credit"

    return "debit"


# --------------------------------------------------------------------
# Transaction Builder
# --------------------------------------------------------------------

def build_transactions(lines):

    transactions = []

    current_date = None
    current_description = []

    previous_balance = None

    for line in lines:

        if is_date_line(line):

            extracted = extract_date(line)

            if extracted is not None:
                current_date = extracted

        if ends_with_amounts(line):

            amounts = extract_amounts(line)

            current_description.append(line)

            description = " ".join(current_description)

            description = re.sub(
                r"\s+",
                " ",
                description
            ).strip()

            # Remove duplicate dates from beginning
            description = re.sub(
                r"^(" + DATE_PATTERN + r")\s*",
                "",
                description,
                flags=re.IGNORECASE,
            )

            description = re.sub(
                r"^(" + DATE_PATTERN + r")\s*",
                "",
                description,
                flags=re.IGNORECASE,
            )

            description = description.strip()

            debit = None
            credit = None
            balance = None

            if len(amounts) >= 2:

                balance = amounts[-1]

                transaction_amount = amounts[-2]

                txn_type = classify_transaction(
                    description,
                    previous_balance,
                    balance,
                )

                if txn_type == "credit":

                    credit = transaction_amount

                else:

                    debit = transaction_amount

            transactions.append(

                TransactionSchema(
                    date=current_date,
                    description=description,
                    debit=debit,
                    credit=credit,
                    balance=balance
                )

            )

            previous_balance = balance

            current_description = []

            continue

        upper = line.upper()

        if upper.startswith("PAGE"):
            continue

        if "DATE DESCRIPTION" in upper:
            continue

        if "DATE VALUE" in upper:
            continue

        current_description.append(line)

    return transactions


# --------------------------------------------------------------------
# OCR Cleanup
# --------------------------------------------------------------------

def preprocess_transaction_text(transaction_text):

    lines = clean_lines(transaction_text)

    cleaned = []

    skip_patterns = [
        "PAGE",
        "DATE DESCRIPTION",
        "DATE VALUE",
        "CHEQUE",
        "BALANCE"
    ]

    for line in lines:

        upper = line.upper()

        ignore = False

        for pattern in skip_patterns:

            if pattern in upper:
                ignore = True
                break

        if ignore:
            continue

        cleaned.append(line)

    return cleaned


# --------------------------------------------------------------------
# Transaction Post Processing
# --------------------------------------------------------------------

def post_process_transactions(transactions):

    cleaned = []

    previous_balance = None

    for transaction in transactions:

        if transaction.balance is None:
            continue

        if transaction.description.strip() == "":
            continue

        if (
            "BALANCE FORWARD" in transaction.description.upper()
            and previous_balance == transaction.balance
        ):
            continue

        previous_balance = transaction.balance

        cleaned.append(transaction)

    return cleaned


# --------------------------------------------------------------------
# Main Extractor
# --------------------------------------------------------------------

def extract_transactions(transaction_text: str):

    lines = preprocess_transaction_text(transaction_text)

    transactions = build_transactions(lines)

    transactions = post_process_transactions(transactions)

    return transactions