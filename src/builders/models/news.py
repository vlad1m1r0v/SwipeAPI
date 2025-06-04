from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.builders.models import Complex


class News(BigIntAuditBase):
    __tablename__ = "news"

    complex_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("complexes.id", ondelete="CASCADE"), unique=True
    )
    title: orm.Mapped[str]
    description: orm.Mapped[str] = sa.Column(sa.Text)

    complex: orm.Mapped["Complex"] = orm.relationship(back_populates="news")
