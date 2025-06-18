from typing import TYPE_CHECKING, List
from decimal import Decimal

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.users.models import User

    from src.builders.models import (
        Infrastructure,
        FormalizationAndPaymentSettings,
        Advantages,
        News,
        Document,
        ComplexGallery,
    )


class Complex(BigIntAuditBase):
    __tablename__ = "complexes"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    name: orm.Mapped[str]
    address: orm.Mapped[str | None]
    description: orm.Mapped[str | None] = sa.Column(sa.Text)
    longitude: orm.Mapped[Decimal | None] = orm.mapped_column(
        sa.Numeric(precision=6, scale=3)
    )
    latitude: orm.Mapped[Decimal | None] = orm.mapped_column(
        sa.Numeric(precision=6, scale=3)
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="complex")
    infrastructure: orm.Mapped["Infrastructure"] = orm.relationship(
        back_populates="complex", uselist=False, cascade="all, delete-orphan"
    )
    formalization_and_payment_settings: orm.Mapped[
        "FormalizationAndPaymentSettings"
    ] = orm.relationship(
        back_populates="complex", uselist=False, cascade="all, delete-orphan"
    )
    advantages: orm.Mapped["Advantages"] = orm.relationship(
        back_populates="complex", uselist=False, cascade="all, delete-orphan"
    )
    news: orm.Mapped[List["News"]] = orm.relationship(
        back_populates="complex", uselist=True, cascade="all, delete-orphan"
    )
    documents: orm.Mapped[List["Document"]] = orm.relationship(
        back_populates="complex", uselist=True, cascade="all, delete-orphan"
    )
    gallery: orm.Mapped[List["ComplexGallery"]] = orm.relationship(
        back_populates="complex", uselist=True, cascade="all, delete-orphan"
    )
