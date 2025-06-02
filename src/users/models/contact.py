from typing import TYPE_CHECKING

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

if TYPE_CHECKING:
    from src.users.models import User


class Contact(BigIntAuditBase):
    __tablename__ = "contacts"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    first_name: orm.Mapped[str | None]
    last_name: orm.Mapped[str | None]
    phone: orm.Mapped[str]
    email: orm.Mapped[str]

    user: orm.Mapped["User"] = orm.relationship(back_populates="contact")
