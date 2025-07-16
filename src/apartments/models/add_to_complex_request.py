from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.builder.models import Riser, Floor

    from src.apartments.models import Apartment


class AddToComplexRequest(BigIntAuditBase):
    __tablename__ = "add_to_complex_requests"

    __table_args__ = (
        sa.UniqueConstraint(
            "apartment_id", "floor_id", "riser_id", name="uq_apartment_floor_riser"
        ),
    )
    apartment_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("apartments.id", ondelete="CASCADE")
    )
    floor_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("floors.id", ondelete="CASCADE")
    )
    riser_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("risers.id", ondelete="CASCADE")
    )

    apartment: orm.Mapped["Apartment"] = orm.relationship(
        back_populates="add_to_complex_requests"
    )
    floor: orm.Mapped["Floor"] = orm.relationship(
        back_populates="add_to_complex_requests"
    )
    riser: orm.Mapped["Riser"] = orm.relationship(
        back_populates="add_to_complex_requests"
    )
