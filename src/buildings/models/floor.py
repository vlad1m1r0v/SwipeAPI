from typing import TYPE_CHECKING, List

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.buildings.models import Block

    from src.apartments.models import Apartment

    from src.requests.models import AddToComplexRequest


class Floor(BigIntAuditBase):
    __tablename__ = "floors"

    __table_args__ = (sa.UniqueConstraint("block_id", "no", name="uq_floor_block_no"),)

    block_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("blocks.id", ondelete="CASCADE")
    )
    no = sa.Column(sa.SmallInteger)

    block: orm.Mapped["Block"] = orm.relationship(back_populates="floors")

    apartments: orm.Mapped[List["Apartment"]] = orm.relationship(
        back_populates="floor",
        uselist=True,
    )
    requests: orm.Mapped[List["AddToComplexRequest"]] = orm.relationship(
        back_populates="floor",
        uselist=True,
        cascade="all, delete-orphan",
    )
