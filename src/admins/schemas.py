from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    EmailStr
)

from src.core.schemas import FileInfo
from src.core.utils.validation import PHONE_NUMBER

from src.users.enums import ROLE


class GetAdminSchema(BaseModel):
    id: int
    name: Optional[str] = Field(min_length=3, max_length=100)
    phone: Optional[str] = Field(pattern=PHONE_NUMBER)
    email: Optional[EmailStr]
    role: ROLE
    photo: Optional[FileInfo]

__all__ = [
    "GetAdminSchema",
]