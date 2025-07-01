from typing import TYPE_CHECKING, List

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.builder.models import Complex, Section, Floor


class Block(BigIntAuditBase):
    __tablename__ = "blocks"

    __table_args__ = (sa.UniqueConstraint("complex_id", "no", name="uq_complex_no"),)

    complex_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("complexes.id", ondelete="CASCADE")
    )
    no = sa.Column(sa.SmallInteger)

    complex: orm.Mapped["Complex"] = orm.relationship(back_populates="blocks")
    sections: orm.Mapped[List["Section"]] = orm.relationship(
        back_populates="block", uselist=True, cascade="all, delete-orphan"
    )
    floors: orm.Mapped[List["Floor"]] = orm.relationship(
        back_populates="block", uselist=True, cascade="all, delete-orphan"
    )
