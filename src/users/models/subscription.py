from typing import TYPE_CHECKING
from datetime import datetime, UTC, timedelta

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.users.models import User


class Subscription(BigIntAuditBase):
    __tablename__ = "subscriptions"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    is_auto_renewal: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    expiry_date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=lambda: datetime.now(UTC).replace(tzinfo=None) + timedelta(days=30)
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="subscription")
