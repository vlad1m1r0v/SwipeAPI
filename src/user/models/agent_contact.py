from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.user.models import User


class AgentContact(BigIntAuditBase):
    __tablename__ = "agent_contacts"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    first_name: orm.Mapped[str | None]
    last_name: orm.Mapped[str | None]
    phone: orm.Mapped[str | None]
    email: orm.Mapped[str | None]

    user: orm.Mapped["User"] = orm.relationship(back_populates="agent_contact")
