from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr
)

from src.core.schemas import FileInfo
from src.users.enums import Role


class GetAdminSchema(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    role: Role
    photo: Optional[FileInfo]