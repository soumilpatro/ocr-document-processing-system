from typing import Dict


TABLE_KEYWORDS = {
    "DATE",
    "VALUE DATE",
    "DESCRIPTION",
    "PARTICULARS",
    "NARRATION",
    "DETAILS",
    "DEBIT",
    "CREDIT",
    "WITHDRAWAL",
    "DEPOSIT",
    "BALANCE",
    "AMOUNT",
}


def find_transaction_table_start(lines):
    """
    Find the line where the transaction table begins.

    Returns:
        Index of the transaction table header.
        Returns -1 if not found.
    """

    best_score = 0
    best_index = -1

    for index, line in enumerate(lines):

        upper = line.upper()

        score = 0

        for keyword in TABLE_KEYWORDS:
            if keyword in upper:
                score += 1

        if score > best_score:
            best_score = score
            best_index = index

    return best_index


def split_document(text: str) -> Dict[str, str]:
    """
    Split OCR text into logical sections.
    """

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    table_start = find_transaction_table_start(lines)

    if table_start == -1:

        return {
            "header": "\n".join(lines),
            "transactions": "",
            "footer": ""
        }

    header = "\n".join(lines[:table_start])

    transactions = "\n".join(lines[table_start:])

    return {
        "header": header,
        "transactions": transactions,
        "footer": ""
    }