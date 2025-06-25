from typing import TYPE_CHECKING, List

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.builders.models import Block, Riser


class Section(BigIntAuditBase):
    __tablename__ = "sections"

    __table_args__ = (
        sa.UniqueConstraint("block_id", "no", name="uq_section_block_no"),
    )

    block_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("blocks.id", ondelete="CASCADE")
    )
    no = sa.Column(sa.SmallInteger)

    block: orm.Mapped["Block"] = orm.relationship(back_populates="sections")
    risers: orm.Mapped[List["Riser"]] = orm.relationship(
        back_populates="section", uselist=True, cascade="all, delete-orphan"
    )
