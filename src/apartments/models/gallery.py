from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.apartments.models import Apartment


class ApartmentGallery(BigIntAuditBase):
    __tablename__ = "apartments_gallery"

    __table_args__ = (
        sa.UniqueConstraint("apartment_id", "order", name="uq_apartment_order"),
    )

    apartment_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("apartments.id", ondelete="CASCADE")
    )
    photo = sa.Column(JSONB)
    order = sa.Column(sa.SmallInteger)

    apartment: orm.Mapped["Apartment"] = orm.relationship(back_populates="gallery")
