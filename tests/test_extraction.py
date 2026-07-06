from app.services.extraction.header_extractor import extract_header
from app.services.extraction.transaction_extractor import extract_transactions


def test_extract_header():

    text = """
    ACCOUNT HOLDER : John Doe
    ACCOUNT NO. : 123456789012
    BRANCH : Mumbai
    IFSC : SBIN0001234
    STATEMENT DATE : 16 Jul 2019
    """

    header = extract_header(text)

    assert header.account_holder is not None
    assert header.account_number == "123456789012"
    assert header.ifsc == "SBIN0001234"


def test_extract_transactions():

    text = """
    01/07/2019 ATM WITHDRAWAL 1000.00 9000.00
    02/07/2019 CASH DEPOSIT 500.00 9500.00
    """

    transactions = extract_transactions(text)

    assert isinstance(transactions, list)