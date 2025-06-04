from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

from src.builders.enums import (
    Formalization,
    BillingOptions,
    PropertyType,
    SumInContract,
)

if TYPE_CHECKING:
    from src.builders.models import Complex


class FormalizationAndPaymentSettings(BigIntAuditBase):
    __tablename__ = "formalization_and_payment_settings"

    complex_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("complexes.id", ondelete="CASCADE"), unique=True
    )
    formalization: orm.Mapped[Formalization] = orm.mapped_column(
        sa.Enum(
            Formalization, name="formalization_and_payment_settings_formalization_enum"
        ),
        nullable=True,
    )
    billing_options: orm.Mapped[BillingOptions] = orm.mapped_column(
        sa.Enum(
            BillingOptions,
            name="formalization_and_payment_settings_billing_options_enum",
        ),
        nullable=True,
    )
    property_type: orm.Mapped[PropertyType] = orm.mapped_column(
        sa.Enum(
            PropertyType, name="formalization_and_payment_settings_property_type_enum"
        ),
        nullable=True,
    )
    sum_in_contract: orm.Mapped[SumInContract] = orm.mapped_column(
        sa.Enum(
            SumInContract,
            name="formalization_and_payment_settings_sum_in_contract_enum",
        ),
        nullable=True,
    )

    complex: orm.Mapped["Complex"] = orm.relationship(
        back_populates="formalization_and_payment_settings"
    )
