from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from advanced_alchemy.base import BigIntAuditBase


if TYPE_CHECKING:
    from src.builder.models import Complex


class ComplexGallery(BigIntAuditBase):
    __tablename__ = "complexes_gallery"

    __table_args__ = (
        sa.UniqueConstraint("complex_id", "order", name="uq_complex_order"),
    )

    complex_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("complexes.id", ondelete="CASCADE")
    )
    photo = sa.Column(JSONB)
    order = sa.Column(sa.SmallInteger)

    complex: orm.Mapped["Complex"] = orm.relationship(back_populates="gallery")
