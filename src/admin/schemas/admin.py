from typing import Optional

from config import config

from pydantic import Field, BaseModel, EmailStr, computed_field

from src.user.enums import Role


class GetAdminSchema(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    role: Role
    photo: Optional[str] = Field(exclude=True)

    @computed_field
    @property
    def photo_url(self) -> Optional[str]:
        return f"{config.server.url}/{self.photo}" if self.photo else None

    class Config:
        from_attributes = True
