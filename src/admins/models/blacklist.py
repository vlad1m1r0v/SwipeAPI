from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase

import sqlalchemy as sa
from sqlalchemy import orm

if TYPE_CHECKING:
    from src.users.models import User


class Blacklist(BigIntAuditBase):
    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    user: orm.Mapped["User"] = orm.relationship(back_populates="blacklist")
