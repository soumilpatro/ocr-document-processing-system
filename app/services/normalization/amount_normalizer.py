import re


def normalize_amount(amount: str) -> float | None:
    """
    Convert OCR amount strings into float values.

    Returns None if conversion is not possible.
    """

    if not amount:
        return None

    amount = amount.strip()

    # Remove currency symbols
    amount = amount.replace("₹", "")
    amount = amount.replace("$", "")
    amount = amount.replace("€", "")

    # Remove commas and spaces
    amount = amount.replace(",", "")
    amount = amount.replace(" ", "")

    # Keep only digits, decimal point and minus sign
    amount = re.sub(r"[^0-9.\-]", "", amount)

    if amount == "":
        return None

    try:
        return float(amount)
    except ValueError:
        return None