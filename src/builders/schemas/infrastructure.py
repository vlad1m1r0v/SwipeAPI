from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

from src.builders.enums import (
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


class UpdateInfrastructureSchema(BaseInfrastructureSchema):
    pass


class GetInfrastructureSchema(BaseInfrastructureSchema):
    id: int
