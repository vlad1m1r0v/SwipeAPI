from advanced_alchemy.base import BigIntAuditBase

import sqlalchemy as sa
from sqlalchemy import orm

from sqlalchemy_file import FileField

from src.core.enums import STORAGE_CONTAINER

from src.users.models import User

class Notary(BigIntAuditBase):
    photo = sa.Column(
        FileField(
            upload_storage=STORAGE_CONTAINER.IMAGES,
        )
    )
    first_name: orm.Mapped[str]
    last_name: orm.Mapped[str]
    email: orm.Mapped[str]
    phone: orm.Mapped[str]


class Blacklist(BigIntAuditBase):
    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    user: orm.Mapped["User"] = orm.relationship(back_populates="blacklist")

__all__ = [
    "Blacklist",
    "Notary"
]
