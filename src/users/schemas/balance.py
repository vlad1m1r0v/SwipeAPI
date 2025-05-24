from pydantic import BaseModel


class GetBalanceSchema(BaseModel):
    id: int
    value: float