from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

from src.builder.enums import (
    Status,
    Type,
    Class,
    Technology,
    Territory,
    UtilityBills,
    Heating,
    Sewerage,
    WaterSupply,
)


class BaseInfrastructureSchema(BaseModel):
    status: Optional[Status] = Field(default=None)
    type: Optional[Type] = Field(default=None)
    infrastructure_class: Optional[Class] = Field(default=None)
    technology: Optional[Technology] = Field(default=None)
    territory: Optional[Territory] = Field(default=None)
    sea_distance: Optional[Decimal] = Field(default=None)
    utility_bills: Optional[UtilityBills] = Field(default=None)
    ceiling_height: Optional[Decimal] = Field(default=None)
    has_gas: Optional[bool] = Field(default=None)
    heating: Optional[Heating] = Field(default=None)
    sewerage: Optional[Sewerage] = Field(default=None)
    water_supply: Optional[WaterSupply] = Field(default=None)


class CreateInfrastructureSchema(BaseModel):
    complex_id: int
    status: Status
    type: Type
    infrastructure_class: Class
    technology: Technology
    territory: Territory
    sea_distance: Decimal
    utility_bills: UtilityBills
    ceiling_height: Decimal
    has_gas: bool
    heating: Heating
    sewerage: Sewerage
    water_supply: WaterSupply


class UpdateInfrastructureSchema(BaseInfrastructureSchema):
    pass


class GetInfrastructureSchema(BaseInfrastructureSchema):
    id: int
