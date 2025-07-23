from typing import TYPE_CHECKING, Optional
from decimal import Decimal

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

from src.builder.enums import (
    Type,
    Status,
    PropertyType,
    BillingOptions,
)

from src.apartments.enums import Rooms, Finishing

if TYPE_CHECKING:
    from src.user.models import User


class Filter(BigIntAuditBase):
    __tablename__ = "filters"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE")
    )

    type: orm.Mapped[Optional[Type]] = orm.mapped_column(
        sa.Enum(Type, name="filter_type_enum"),
        nullable=True,
    )
    status: orm.Mapped[Optional[Status]] = orm.mapped_column(
        sa.Enum(Status, name="filter_status_enum"),
        nullable=True,
    )
    district: orm.Mapped[Optional[str]] = orm.mapped_column(nullable=True)
    neighborhood: orm.Mapped[Optional[str]] = orm.mapped_column(nullable=True)
    rooms: orm.Mapped[Optional[Rooms]] = orm.mapped_column(
        sa.Enum(Rooms, name="filter_rooms_enum"),
        nullable=True,
    )
    price_min: orm.Mapped[Optional[int]] = orm.mapped_column(nullable=True)
    price_max: orm.Mapped[Optional[int]] = orm.mapped_column(nullable=True)
    area_min: orm.Mapped[Optional[Decimal]] = orm.mapped_column(nullable=True)
    area_max: orm.Mapped[Optional[Decimal]] = orm.mapped_column(nullable=True)
    property_type: orm.Mapped[Optional[PropertyType]] = orm.mapped_column(
        sa.Enum(PropertyType, name="filter_property_type_enum"),
        nullable=True,
    )
    billing_options: orm.Mapped[Optional[BillingOptions]] = orm.mapped_column(
        sa.Enum(BillingOptions, name="filter_billing_options_enum"),
        nullable=True,
    )
    finishing: orm.Mapped[Optional[Finishing]] = orm.mapped_column(
        sa.Enum(Finishing, name="filter_finishing_enum"),
        nullable=True,
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="filters")
