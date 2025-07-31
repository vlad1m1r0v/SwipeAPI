from typing import List, Optional

from pydantic import BaseModel, Field, computed_field

from src.apartments.enums import Rooms

from src.core.schemas import GetGalleryImageSchema

from src.user.schemas import GetContactSchema


class CreateAddToComplexRequest(BaseModel):
    apartment_id: int
    riser_id: int
    floor_id: int


class GetBuilderBlockSchema(BaseModel):
    id: int
    no: int


class GetBuilderFloorSchema(BaseModel):
    id: int
    no: int
    block: GetBuilderBlockSchema


class GetRiserSchema(BaseModel):
    id: int
    no: int


class GetUserSchema(BaseModel):
    id: int
    contact: GetContactSchema


class GetBuilderApartmentSchema(BaseModel):
    id: int
    gallery: List[GetGalleryImageSchema] = Field(exclude=True)
    price: int
    rooms: Rooms
    area: float
    address: str
    user: GetUserSchema

    @computed_field
    @property
    def preview_url(self) -> Optional[str]:
        return self.gallery[0].photo_url if len(self.gallery) else None


class GetAddToComplexRequestBuilderSchema(BaseModel):
    id: int
    floor: GetBuilderFloorSchema
    riser: GetRiserSchema
    apartment: GetBuilderApartmentSchema


class GetUserComplexSchema(BaseModel):
    id: int
    name: str


class GetUserBlockSchema(BaseModel):
    id: int
    no: int
    complex: GetUserComplexSchema


class GetUserFloorSchema(BaseModel):
    id: int
    no: int
    block: GetUserBlockSchema


class GetUserApartmentSchema(BaseModel):
    id: int
    gallery: List[GetGalleryImageSchema] = Field(exclude=True)
    price: int
    rooms: Rooms
    area: float
    address: str

    @computed_field
    @property
    def preview_url(self) -> Optional[str]:
        return self.gallery[0].photo_url if len(self.gallery) else None


class GetAddToComplexRequestUserSchema(BaseModel):
    id: int
    floor: GetUserFloorSchema
    riser: GetRiserSchema
    apartment: GetUserApartmentSchema
