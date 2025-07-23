from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.announcements.models import Announcement

    from src.user.models import User


class Complaint(BigIntAuditBase):
    __tablename__ = "complaints"

    announcement_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("announcements.id", ondelete="CASCADE"),
    )
    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
    )

    is_incorrect_price: orm.Mapped[bool]
    is_incorrect_photo: orm.Mapped[bool]
    is_incorrect_description: orm.Mapped[bool]

    announcement: orm.Mapped["Announcement"] = orm.relationship(
        back_populates="complaints"
    )
    user: orm.Mapped["User"] = orm.relationship(back_populates="complaints")
