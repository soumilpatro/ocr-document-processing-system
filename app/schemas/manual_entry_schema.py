from typing import List

from pydantic import BaseModel


class StatementPeriod(BaseModel):
    from_date: str | None = None
    to_date: str | None = None


class ManualTransactionSchema(BaseModel):
    date: str
    description: str
    debit: float | None = None
    credit: float | None = None
    balance: float


class ManualEntrySchema(BaseModel):

    account_holder: str | None = None

    account_number: str | None = None

    branch: str | None = None

    ifsc: str | None = None

    statement_date: str | None = None

    statement_period: StatementPeriod = StatementPeriod()

    transactions: List[ManualTransactionSchema]