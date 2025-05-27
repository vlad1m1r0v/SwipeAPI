from typing import Optional

from pydantic import (
    Field,
    BaseModel,
    EmailStr,
    computed_field
)

from src.core.schemas import FileInfo
from src.users.enums import Role


class GetAdminSchema(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    role: Role
    photo: Optional[FileInfo] = Field(exclude=True)

    @computed_field
    @property
    def photo_url(self) -> Optional[str]:
        return self.photo.url if self.photo.url else None

    class Config:
        from_attributes = True
