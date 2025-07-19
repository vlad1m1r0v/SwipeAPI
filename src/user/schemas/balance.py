from pydantic import BaseModel, Field


class DepositBalanceSchema(BaseModel):
    amount: int = Field(le=9999)


class CreateBalanceSchema(BaseModel):
    user_id: int
    value: float


class GetBalanceSchema(BaseModel):
    id: int
    value: float
