from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase

import sqlalchemy as sa
from sqlalchemy import orm

if TYPE_CHECKING:
    from src.user.models import User


class Blacklist(BigIntAuditBase):
    user_id = orm.mapped_column(
        sa.BigInteger,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )
    user: orm.Mapped["User"] = orm.relationship(back_populates="blacklist")
