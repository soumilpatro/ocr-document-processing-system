import csv
from io import StringIO

from app.schemas.manual_entry_schema import (
    ManualEntrySchema,
    ManualTransactionSchema,
    StatementPeriod,
)


def parse_csv(file_contents: str):

    reader = csv.DictReader(StringIO(file_contents))

    rows = list(reader)

    if not rows:
        return []

    first = rows[0]

    transactions = []

    for row in rows:

        transactions.append(

            ManualTransactionSchema(

                date=row["txn_date"],

                description=row["description"],

                debit=float(row["debit"])
                if row["debit"] else None,

                credit=float(row["credit"])
                if row["credit"] else None,

                balance=float(row["balance"])

            )

        )

    document = ManualEntrySchema(

        account_holder=first["account_holder"],

        account_number=first["account_number"],

        branch=first["branch"],

        ifsc=first["ifsc"],

        statement_date=first["statement_date"],

        statement_period=StatementPeriod(

            from_date=first["statement_from"],

            to_date=first["statement_to"]

        ),

        transactions=transactions,

    )

    return [document]