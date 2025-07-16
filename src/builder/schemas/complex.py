from typing import Optional
from decimal import Decimal
from pydantic import BaseModel

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


class GetComplexSchema(BaseComplexSchema):
    id: int
    infrastructure: GetInfrastructureSchema
    advantages: GetAdvantagesSchema
    formalization_and_payment_settings: GetFormalizationAndPaymentSettingsSchema
    news: Optional[list[GetNewsSchema]] = []
    documents: Optional[list[GetDocumentSchema]] = []
    gallery: Optional[list[GetGalleryImageSchema]] = []


class GetComplexIdAndNoSchema(BaseModel):
    id: int
    name: str


class GetBuilderSchema(GetUserAccountSchema):
    contact: GetContactSchema
    complex: GetComplexSchema
