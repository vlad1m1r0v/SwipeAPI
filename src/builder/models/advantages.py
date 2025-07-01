from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.builder.models import Complex


class Advantages(BigIntAuditBase):
    __tablename__ = "advantages"

    complex_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("complexes.id", ondelete="CASCADE"), unique=True
    )
    has_children_playground: orm.Mapped[bool | None]
    has_sports_field: orm.Mapped[bool | None]
    has_parking: orm.Mapped[bool | None]
    has_landscaped_area: orm.Mapped[bool | None]
    has_on_site_shops: orm.Mapped[bool | None]
    has_individual_heating: orm.Mapped[bool | None]
    has_balcony_or_loggia: orm.Mapped[bool | None]
    has_bicycle_field: orm.Mapped[bool | None]
    has_panoramic_windows: orm.Mapped[bool | None]
    is_close_to_sea: orm.Mapped[bool | None]
    is_close_to_school: orm.Mapped[bool | None]
    is_close_to_transport: orm.Mapped[bool | None]

    complex: orm.Mapped["Complex"] = orm.relationship(back_populates="advantages")
