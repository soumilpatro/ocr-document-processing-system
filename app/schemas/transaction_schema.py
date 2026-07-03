from pydantic import BaseModel


class TransactionSchema(BaseModel):

    date: str | None = None

    description: str | None = None

    debit: float | None = None

    credit: float | None = None

    balance: float | None = None