from typing import List, Optional

from pydantic import BaseModel, Field, computed_field

from config import config

from src.core.schemas import GetGalleryImageSchema

from src.user.schemas import GetContactSchema


class FloorSchema(BaseModel):
    no: int


class RiserSchema(BaseModel):
    no: int


class UserSchema(BaseModel):
    contact: GetContactSchema = Field(exclude=True)

    photo: Optional[str] = Field(exclude=True, default=None)

    @computed_field
    @property
    def photo_url(self) -> Optional[str]:
        return f"{config.server.url}/{self.photo}" if self.photo else None

    @computed_field
    @property
    def first_name(self) -> Optional[str]:
        return self.contact.first_name

    @computed_field
    @property
    def last_name(self) -> Optional[str]:
        return self.contact.last_name

    @computed_field
    @property
    def phone(self) -> Optional[str]:
        return self.contact.phone

    @computed_field
    @property
    def email(self) -> Optional[str]:
        return self.contact.email


class ApartmentSchema(BaseModel):
    address: str
    longitude: float
    latitude: float
    area: float
    price: int
    gallery: List[GetGalleryImageSchema] = Field(exclude=True)
    user: UserSchema

    @computed_field
    @property
    def preview_url(self) -> Optional[str]:
        return self.gallery[0].photo_url if len(self.gallery) else None


class AddToComplexRequestSchema(BaseModel):
    id: int
    floor: FloorSchema = Field(exclude=True)
    riser: RiserSchema = Field(exclude=True)
    apartment: ApartmentSchema

    @computed_field
    @property
    def floor_no(self) -> int:
        return self.floor.no

    @computed_field
    @property
    def riser_no(self) -> int:
        return self.riser.no
