from app.schemas import HeaderSchema
from app.schemas import TransactionSchema


def validate_header(header: HeaderSchema):

    errors = []

    if not header.account_holder:
        errors.append("Account holder missing")

    if not header.account_number:
        errors.append("Account number missing")

    return errors


def validate_transactions(transactions: list[TransactionSchema]):

    errors = []

    for index, txn in enumerate(transactions):

        if txn.date is None:
            errors.append(
                f"Transaction {index + 1}: Missing date"
            )

        if txn.balance is None:
            errors.append(
                f"Transaction {index + 1}: Missing balance"
            )

        if txn.debit is None and txn.credit is None:
            errors.append(
                f"Transaction {index + 1}: Missing amount"
            )

    return errors


def validate_document(header, transactions):

    header_errors = validate_header(header)
    transaction_errors = validate_transactions(transactions)

    return {

        "status": "VALID"
        if not header_errors and not transaction_errors
        else "INVALID",

        "header": header_errors,

        "transactions": transaction_errors,

        "totalErrors": len(header_errors) + len(transaction_errors),

    }