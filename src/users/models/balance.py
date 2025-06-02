from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

import src.users.constants as constants

if TYPE_CHECKING:
    from src.users.models import User


class Balance(BigIntAuditBase):
    __tablename__ = "balances"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    value: orm.Mapped[Decimal] = orm.mapped_column(
        sa.Numeric(precision=12, scale=2), default=constants.DEFAULT_BALANCE
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="balance")
