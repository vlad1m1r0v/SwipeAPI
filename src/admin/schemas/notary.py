from typing import Optional

from pydantic import BaseModel, Field, EmailStr, computed_field

from src.core.schemas import FileInfo
from src.core.constants import PHONE_NUMBER


class CreateNotarySchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    phone: str = Field(pattern=PHONE_NUMBER)
    email: EmailStr
    photo: Optional[FileInfo]


class UpdateNotarySchema(BaseModel):
    first_name: Optional[str] = Field(min_length=3, max_length=100)
    last_name: Optional[str] = Field(min_length=3, max_length=100)
    phone: Optional[str] = Field(pattern=PHONE_NUMBER)
    email: Optional[EmailStr]
    photo: Optional[FileInfo]


class GetNotarySchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    photo: Optional[FileInfo] = Field(exclude=True)

    @computed_field
    @property
    def photo_url(self) -> Optional[str]:
        return self.photo.url if self.photo else None

    class Config:
        from_attributes = True
