from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base
from src.users.enums import NotificationTypeEnum

if TYPE_CHECKING:
    from .user import UserModel

class NotificationSettingsModel(Base):
    __tablename__ = "notification_settings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    redirect_notifications_to_agent: Mapped[bool] = mapped_column(Boolean, default=False)
    notification_type: Mapped[NotificationTypeEnum] = mapped_column(
        Enum(NotificationTypeEnum, name="notification_type_enum"),
        nullable=False,
        default=NotificationTypeEnum.DISABLED,
    )

    user: Mapped["UserModel"] = relationship(back_populates="notification_settings")