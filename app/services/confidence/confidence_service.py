from app.schemas.header_schema import HeaderSchema
from app.schemas.transaction_schema import TransactionSchema


def confidence_from_value(value):

    if value is None:
        return 0.0

    if isinstance(value, str):

        value = value.strip()

        if value == "":
            return 0.0

        return 0.95

    return 0.98


def header_confidence(header: HeaderSchema):

    return {

        "account_holder":
            confidence_from_value(header.account_holder),

        "account_number":
            confidence_from_value(header.account_number),

        "branch":
            confidence_from_value(header.branch),

        "ifsc":
            confidence_from_value(header.ifsc),

        "statement_date":
            confidence_from_value(header.statement_date),

        "statement_period": {

            "from_date":
                confidence_from_value(
                    header.statement_period.from_date
                ),

            "to_date":
                confidence_from_value(
                    header.statement_period.to_date
                )

        }

    }


def transaction_confidence(transaction: TransactionSchema):

    # -----------------------------
    # Debit / Credit Logic
    # -----------------------------

    if transaction.debit is None and transaction.credit is None:

        debit_confidence = 0.0
        credit_confidence = 0.0

    else:

        # One side being empty is expected
        debit_confidence = 0.98
        credit_confidence = 0.98

    return {

        "date":
            confidence_from_value(transaction.date),

        "description":
            confidence_from_value(transaction.description),

        "debit":
            debit_confidence,

        "credit":
            credit_confidence,

        "balance":
            confidence_from_value(transaction.balance)

    }


def overall_confidence(header, transactions):

    header_scores = header_confidence(header)

    transaction_scores = [

        transaction_confidence(txn)

        for txn in transactions

    ]

    scores = []

    # -------------------------
    # Header Scores
    # -------------------------

    for key, value in header_scores.items():

        if isinstance(value, dict):

            scores.extend(value.values())

        else:

            scores.append(value)

    # -------------------------
    # Transaction Scores
    # -------------------------

    for txn in transaction_scores:

        scores.extend(txn.values())

    overall = round(

        (sum(scores) / len(scores)) * 100,

        2

    )

    return {

        "overall": overall,

        "header": header_scores,

        "transactions": transaction_scores

    }