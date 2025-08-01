from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.builder.models import Complex

    from src.user.models import User


class FavouriteComplex(BigIntAuditBase):
    __tablename__ = "favourite_complexes"
    __table_args__ = (
        sa.UniqueConstraint("user_id", "complex_id", name="uq_user_complex"),
    )

    complex_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("complexes.id", ondelete="CASCADE"),
    )
    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
    )

    complex: orm.Mapped["Complex"] = orm.relationship(
        back_populates="favourite_complexes"
    )
    user: orm.Mapped["User"] = orm.relationship(back_populates="favourite_complexes")
