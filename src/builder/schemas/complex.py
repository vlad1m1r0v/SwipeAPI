from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, computed_field

from .infrastructure import GetInfrastructureSchema
from .advantages import GetAdvantagesSchema
from .formalization_and_payment_settings import GetFormalizationAndPaymentSettingsSchema
from .news import GetNewsSchema
from .document import GetDocumentSchema

from src.core.schemas import GetGalleryImageSchema

from src.user.schemas import GetUserAccountSchema, GetContactSchema


class BaseComplexSchema(BaseModel):
    name: Optional[str]
    address: Optional[str]
    description: Optional[str]
    longitude: Optional[Decimal]
    latitude: Optional[Decimal]


class UpdateComplexSchema(BaseComplexSchema):
    pass


class BlockWithApartmentsCountSchema(BaseModel):
    id: int
    no: int
    apartments_count: int


class GetComplexSchema(BaseComplexSchema):
    id: int
    min_price: int
    avg_price_per_m2: float
    min_area: float
    max_area: float
    apartments_per_block: Optional[list[BlockWithApartmentsCountSchema]] = []
    infrastructure: GetInfrastructureSchema
    advantages: GetAdvantagesSchema
    formalization_and_payment_settings: GetFormalizationAndPaymentSettingsSchema
    news: Optional[list[GetNewsSchema]] = []
    documents: Optional[list[GetDocumentSchema]] = []
    gallery: Optional[list[GetGalleryImageSchema]] = []

    @field_validator("avg_price_per_m2", mode="before")
    def round_avg_price(cls, v):
        return round(v)


class GetBuilderSchema(GetUserAccountSchema):
    contact: GetContactSchema
    complex: GetComplexSchema


class GetComplexFeedListItemSchema(BaseModel):
    id: int
    name: str
    address: str
    min_price: int
    min_area: float
    gallery: Optional[list[GetGalleryImageSchema]] = Field(exclude=True)

    @computed_field
    @property
    def preview_url(self) -> Optional[str]:
        return self.gallery[0].photo_url if len(self.gallery) else None


class GetComplexFeedDetailSchema(GetComplexSchema):
    phone: str
