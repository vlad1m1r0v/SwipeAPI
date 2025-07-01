from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.builder.models import Complex


class Document(BigIntAuditBase):
    __tablename__ = "documents"

    complex_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("complexes.id", ondelete="CASCADE")
    )
    name: orm.Mapped[str]
    file = sa.Column(JSONB)

    complex: orm.Mapped["Complex"] = orm.relationship(back_populates="documents")
