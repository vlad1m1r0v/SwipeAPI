from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.apartments.models import Apartment

    from src.announcements.models import (
        AnnouncementView,
        Complaint,
        FavouriteAnnouncement,
        Promotion,
    )


class Announcement(BigIntAuditBase):
    __tablename__ = "announcements"

    apartment_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("apartments.id", ondelete="CASCADE"), unique=True
    )
    is_relevant: bool = sa.Column(sa.Boolean, default=True)
    is_approved: orm.Mapped[bool | None]
    viewing_time = sa.Column(sa.Time)

    apartment: orm.Mapped["Apartment"] = orm.relationship(back_populates="announcement")
    promotion: orm.Mapped["Promotion"] = orm.relationship(
        back_populates="announcement",
        uselist=False,
        cascade="all, delete-orphan",
    )
    views: orm.Mapped[list["AnnouncementView"]] = orm.relationship(
        uselist=True, back_populates="announcement", cascade="all, delete-orphan"
    )
    complaints: orm.Mapped[list["Complaint"]] = orm.relationship(
        uselist=True, back_populates="announcement", cascade="all, delete-orphan"
    )
    favourite_announcements: orm.Mapped[list["FavouriteAnnouncement"]] = (
        orm.relationship(
            back_populates="announcement",
            cascade="all, delete-orphan",
        )
    )
