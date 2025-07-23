from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.announcements.models import Announcement

    from src.user.models import User


class AnnouncementView(BigIntAuditBase):
    __tablename__ = "views"

    announcement_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("announcements.id", ondelete="CASCADE"),
    )
    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
    )

    announcement: orm.Mapped["Announcement"] = orm.relationship(back_populates="views")
    user: orm.Mapped["User"] = orm.relationship(back_populates="views")
