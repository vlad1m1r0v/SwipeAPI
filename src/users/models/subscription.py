from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from .user import UserModel

class SubscriptionModel(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    is_auto_renewal: Mapped[bool] = mapped_column(Boolean, default=False)
    expiry_date: Mapped[datetime]

    user: Mapped["UserModel"] = relationship(back_populates="subscription")