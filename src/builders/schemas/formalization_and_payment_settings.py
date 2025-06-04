from typing import Optional
from pydantic import BaseModel, Field

from src.builders.enums import (
    Formalization,
    BillingOptions,
    PropertyType,
    SumInContract,
)


class BaseFormalizationAndPaymentSettingsSchema(BaseModel):
    formalization: Optional[Formalization] = Field(default=None)
    billing_options: Optional[BillingOptions] = Field(default=None)
    property_type: Optional[PropertyType] = Field(default=None)
    sum_in_contract: Optional[SumInContract] = Field(default=None)


class UpdateFormalizationAndPaymentSettingsSchema(
    BaseFormalizationAndPaymentSettingsSchema
):
    pass


class GetFormalizationAndPaymentSettingsSchema(
    BaseFormalizationAndPaymentSettingsSchema
):
    id: int
