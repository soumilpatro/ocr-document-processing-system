from pydantic import BaseModel


class StatementPeriod(BaseModel):
    from_date: str | None = None
    to_date: str | None = None


class HeaderSchema(BaseModel):
    account_holder: str | None = None
    account_number: str | None = None
    branch: str | None = None
    ifsc: str | None = None
    statement_date: str | None = None
    statement_period: StatementPeriod = StatementPeriod()