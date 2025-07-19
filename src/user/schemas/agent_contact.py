from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from src.core.constants import PHONE_NUMBER


class CreateAgentContactSchema(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    phone: str
    email: EmailStr


class UpdateAgentContactSchema(BaseModel):
    first_name: Optional[str] = Field(min_length=3, max_length=100, default=None)
    last_name: Optional[str] = Field(min_length=3, max_length=100, default=None)
    phone: Optional[str] = Field(pattern=PHONE_NUMBER, default=None)
    email: Optional[EmailStr] = Field(default=None)


class GetAgentContactSchema(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    phone: str | None
    email: str | None
