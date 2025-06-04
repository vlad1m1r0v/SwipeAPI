from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

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

if TYPE_CHECKING:
    from src.builders.models import Complex


class Infrastructure(BigIntAuditBase):
    __tablename__ = "infrastructures"

    complex_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("complexes.id", ondelete="CASCADE"), unique=True
    )
    status: orm.Mapped[Status] = orm.mapped_column(
        sa.Enum(Status, name="infrastructure_status_enum"), nullable=True
    )
    type: orm.Mapped[Type] = orm.mapped_column(
        sa.Enum(Type, name="infrastructure_type_enum"), nullable=True
    )
    infrastructure_class: orm.Mapped[Class] = orm.mapped_column(
        sa.Enum(Class, name="infrastructure_class_enum"), nullable=True
    )
    technology: orm.Mapped[Technology] = orm.mapped_column(
        sa.Enum(Technology, name="infrastructure_technology_enum"), nullable=True
    )
    territory: orm.Mapped[Territory] = orm.mapped_column(
        sa.Enum(Territory, name="infrastructure_territory_enum"), nullable=True
    )
    sea_distance: orm.Mapped[Decimal | None] = orm.mapped_column(
        sa.Numeric(precision=6, scale=3)
    )
    utility_bills: orm.Mapped[UtilityBills] = orm.mapped_column(
        sa.Enum(UtilityBills, name="infrastructure_utility_bills_enum"), nullable=True
    )
    ceiling_height: orm.Mapped[Decimal | None] = orm.mapped_column(
        sa.Numeric(precision=3, scale=2)
    )
    has_gas: orm.Mapped[bool | None]
    heating: orm.Mapped[Heating] = orm.mapped_column(
        sa.Enum(Heating, name="infrastructure_heating_enum"), nullable=True
    )
    sewerage: orm.Mapped[Sewerage] = orm.mapped_column(
        sa.Enum(Sewerage, name="infrastructure_sewerage_enum"), nullable=True
    )
    water_supply: orm.Mapped[WaterSupply] = orm.mapped_column(
        sa.Enum(WaterSupply, name="infrastructure_water_supply_enum"), nullable=True
    )

    complex: orm.Mapped["Complex"] = orm.relationship(back_populates="infrastructure")
