from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel, Field, computed_field

from config import config

from src.builder.enums import Technology, PropertyType, Heating
from src.builder.schemas import GetRiserSchema

from src.apartments.enums import (
    OwnershipType,
    Bedrooms,
    Bathrooms,
    Commission,
    ApartmentCondition,
    Finishing,
    Rooms,
    CallMethod,
)

from src.core.schemas import Base64Item, GetGalleryImageSchema


class CreateApartmentSchema(BaseModel):
    address: str
    longitude: float
    latitude: float
    district: str
    microdistrict: str
    technology: Technology
    property_type: PropertyType
    ownership_type: OwnershipType
    bedrooms: Bedrooms
    bathrooms: Bathrooms
    kitchen_area: float
    heating: Heating
    has_balcony_or_loggia: bool
    has_mortgage: bool
    commission_to_agent: Commission
    condition: ApartmentCondition
    finishing: Finishing
    rooms: Rooms
    area: float
    call_method: CallMethod
    description: str
    price: int
    # base64 string
    scheme: str = Field(
        examples=[
            "data:image/webp;base64,UklGRsYBAABXRUJQVlA4ILoBAAAQBwCdASoZABkAPlEkj0WjoiEUBAA4BQSxgE6ZcQwMtSrgDId+zdj09sCsqOL727JpXxkUk+fXSI8XTKRcmPOoAAD+9WPEOt/QRkR0Fx/6jYW3Ph2WvqZb/WNSAy5f5bTlVdONzxFXAu39tFlQLHk2O22XpgsgRtmCKASeHVHf6VUjUXkqH9pBp3uZlomESkDt2YAwj3EmJGufzx1FNKtdEjvZ1ChhmZs9Avd3PNJNwvHz9Pw986RmTZ750TTyjUn0gQHEYzAK63blnz4pP3M6Rw9zbXm1BVKHYpBWwpGb4vviA90o8iScc+6/xB6i1BBt/Jh5H+KUdoP+Oa+9duR/9WuCz9LOYfce8PPvbctf/ZyCbESy1YIMqYf9SuSbkw/ao3lpwfUfUArZvSf/lzqn6d473t+UNiOXh1V2fvlQK+lOBMEX4qT/6F2I/f/SEK9n4N9uKxZeCg6VXd3kUNI4uGwIEnDw55eLX4BVSmfTxVPPk5uKBJpmPhqeYcILa+fZ8nHTDr7YrojLSTLumbimf2Xkk5+XrJ7wWB+z5xtYel8f/zYxdusDu9K/uf+Lhh6P7lv5O/1jCAAA"
        ]
    )
    gallery: List[Base64Item]


class UpdateApartmentSchema(BaseModel):
    address: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    district: Optional[str]
    microdistrict: Optional[str]
    technology: Optional[Technology]
    property_type: Optional[PropertyType]
    ownership_type: Optional[OwnershipType]
    bedrooms: Optional[Bedrooms]
    bathrooms: Optional[Bathrooms]
    kitchen_area: Optional[float]
    heating: Optional[Heating]
    has_balcony_or_loggia: Optional[bool]
    has_mortgage: Optional[bool]
    commission_to_agent: Optional[Commission]
    condition: Optional[ApartmentCondition]
    finishing: Optional[Finishing]
    rooms: Optional[Rooms]
    area: Optional[float]
    call_method: Optional[CallMethod]
    description: Optional[str]
    price: Optional[int]
    # base64 string
    scheme: Optional[str] = Field(
        examples=[
            "data:image/webp;base64,UklGRsYBAABXRUJQVlA4ILoBAAAQBwCdASoZABkAPlEkj0WjoiEUBAA4BQSxgE6ZcQwMtSrgDId+zdj09sCsqOL727JpXxkUk+fXSI8XTKRcmPOoAAD+9WPEOt/QRkR0Fx/6jYW3Ph2WvqZb/WNSAy5f5bTlVdONzxFXAu39tFlQLHk2O22XpgsgRtmCKASeHVHf6VUjUXkqH9pBp3uZlomESkDt2YAwj3EmJGufzx1FNKtdEjvZ1ChhmZs9Avd3PNJNwvHz9Pw986RmTZ750TTyjUn0gQHEYzAK63blnz4pP3M6Rw9zbXm1BVKHYpBWwpGb4vviA90o8iScc+6/xB6i1BBt/Jh5H+KUdoP+Oa+9duR/9WuCz9LOYfce8PPvbctf/ZyCbESy1YIMqYf9SuSbkw/ao3lpwfUfUArZvSf/lzqn6d473t+UNiOXh1V2fvlQK+lOBMEX4qT/6F2I/f/SEK9n4N9uKxZeCg6VXd3kUNI4uGwIEnDw55eLX4BVSmfTxVPPk5uKBJpmPhqeYcILa+fZ8nHTDr7YrojLSTLumbimf2Xkk5+XrJ7wWB+z5xtYel8f/zYxdusDu9K/uf+Lhh6P7lv5O/1jCAAA"
        ]
    )
    gallery: Optional[List[Base64Item]]


class GetFloorSchema(BaseModel):
    id: int
    no: int


class GetApartmentItemSchema(BaseModel):
    id: int
    address: str
    area: float
    price: float
    floor: GetFloorSchema | None = Field(exclude=True)
    riser: GetRiserSchema | None = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def block_no(self) -> Optional[int]:
        return self.riser.section.block.no if self.floor else None

    @computed_field
    @property
    def floor_no(self) -> Optional[int]:
        return self.floor.no if self.floor else None

    @computed_field
    @property
    def section_no(self) -> Optional[int]:
        return self.riser.section.no if self.riser else None

    @computed_field
    @property
    def riser_no(self) -> Optional[int]:
        return self.riser.no if self.riser else None


class GetApartmentDetailsSchema(BaseModel):
    id: int
    address: str
    longitude: float
    latitude: float
    district: str
    microdistrict: str
    technology: Technology
    property_type: PropertyType
    ownership_type: OwnershipType
    bedrooms: Bedrooms
    bathrooms: Bathrooms
    kitchen_area: float
    heating: Heating
    has_balcony_or_loggia: bool
    has_mortgage: bool
    commission_to_agent: Commission
    condition: ApartmentCondition
    finishing: Finishing
    rooms: Rooms
    area: float
    call_method: CallMethod
    description: str
    price: int
    scheme: str = Field(exclude=True)
    gallery: List[GetGalleryImageSchema]

    floor: GetFloorSchema | None = Field(exclude=True)
    riser: GetRiserSchema | None = Field(exclude=True)

    @computed_field
    @property
    def block_no(self) -> Optional[int]:
        return self.riser.section.block.no if self.floor else None

    @computed_field
    @property
    def floor_no(self) -> Optional[int]:
        return self.floor.no if self.floor else None

    @computed_field
    @property
    def section_no(self) -> Optional[int]:
        return self.riser.section.no if self.riser else None

    @computed_field
    @property
    def riser_no(self) -> Optional[int]:
        return self.riser.no if self.riser else None

    @computed_field
    @property
    def scheme_url(self) -> Optional[str]:
        return f"{config.server.url}/{self.scheme}" if self.scheme else None
