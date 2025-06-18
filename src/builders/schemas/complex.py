from typing import Optional
from decimal import Decimal
from pydantic import BaseModel

from .infrastructure import GetInfrastructureSchema
from .advantages import GetAdvantagesSchema
from .formalization_and_payment_settings import GetFormalizationAndPaymentSettingsSchema
from .news import GetNewsSchema

from src.users.schemas import GetUserAccountSchema, GetContactSchema


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


class GetBuilderSchema(GetUserAccountSchema):
    contact: GetContactSchema
    complex: GetComplexSchema
