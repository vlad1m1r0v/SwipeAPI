from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.announcements.models import Announcement

    from src.user.models import User


class FavouriteAnnouncement(BigIntAuditBase):
    __tablename__ = "favourite_announcements"

    announcement_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("announcements.id", ondelete="CASCADE"),
    )
    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
    )

    announcement: orm.Mapped["Announcement"] = orm.relationship(
        back_populates="favourite_announcements"
    )
    user: orm.Mapped["User"] = orm.relationship(
        back_populates="favourite_announcements"
    )
