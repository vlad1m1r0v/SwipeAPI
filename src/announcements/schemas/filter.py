from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from src.builder.enums import (
    Type,
    Status,
    PropertyType,
    BillingOptions,
)

from src.apartments.enums import Rooms, Finishing


class BaseFilterSchema(BaseModel):
    type: Optional[Type] = None
    status: Optional[Status] = None
    district: Optional[str] = None
    neighborhood: Optional[str] = None
    rooms: Optional[Rooms] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    area_min: Optional[Decimal] = None
    area_max: Optional[Decimal] = None
    property_type: Optional[PropertyType] = None
    billing_options: Optional[BillingOptions] = None
    finishing: Optional[Finishing] = None


class CreateFilterSchema(BaseFilterSchema):
    pass


class UpdateFilterSchema(BaseFilterSchema):
    pass


class GetFilterSchema(BaseFilterSchema):
    id: int
