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

    return {

        "date":
            confidence_from_value(transaction.date),

        "description":
            confidence_from_value(transaction.description),

        "debit":
            confidence_from_value(transaction.debit),

        "credit":
            confidence_from_value(transaction.credit),

        "balance":
            confidence_from_value(transaction.balance)

    }


def overall_confidence(header, transactions):

    return {

        "header": header_confidence(header),

        "transactions": [

            transaction_confidence(txn)

            for txn in transactions

        ]

    }