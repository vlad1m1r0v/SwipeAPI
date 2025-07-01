from typing import TYPE_CHECKING
from datetime import datetime, UTC

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

from src.user.constants import MONTH_DELTA

if TYPE_CHECKING:
    from src.user.models import User


class Subscription(BigIntAuditBase):
    __tablename__ = "subscriptions"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    is_auto_renewal: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    expiry_date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=lambda: datetime.now(UTC).replace(tzinfo=None) + MONTH_DELTA,
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="subscription")
