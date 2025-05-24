from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

from src.users.enums import NotificationType

if TYPE_CHECKING:
    from src.users.models import User


class NotificationSettings(BigIntAuditBase):
    __tablename__ = "notification_settings"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    redirect_notifications_to_agent: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    notification_type: orm.Mapped[NotificationType] = orm.mapped_column(
        sa.Enum(NotificationType, name="notification_type_enum"),
        nullable=False,
        default=NotificationType.DISABLED,
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="notification_settings")
