from pydantic import BaseModel, Field


class DepositBalanceSchema(BaseModel):
    amount: int = Field(le=9999)


class GetBalanceSchema(BaseModel):
    id: int
    value: float
