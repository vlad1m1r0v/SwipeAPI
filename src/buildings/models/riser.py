from typing import TYPE_CHECKING, List

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.buildings.models import Section

    from src.apartments.models import Apartment

    from src.requests.models import AddToComplexRequest


class Riser(BigIntAuditBase):
    __tablename__ = "risers"

    __table_args__ = (sa.UniqueConstraint("section_id", "no", name="uq_section_no"),)

    section_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("sections.id", ondelete="CASCADE")
    )
    no = sa.Column(sa.SmallInteger)

    section: orm.Mapped["Section"] = orm.relationship(back_populates="risers")
    apartments: orm.Mapped[List["Apartment"]] = orm.relationship(
        back_populates="riser",
        uselist=True,
    )

    requests: orm.Mapped[List["AddToComplexRequest"]] = orm.relationship(
        back_populates="riser",
        uselist=True,
        cascade="all, delete-orphan",
    )
