from typing import Optional

from advanced_alchemy.base import BigIntAuditBase

from sqlalchemy import orm


class Notary(BigIntAuditBase):
    photo: orm.Mapped[Optional[str]] = orm.mapped_column(nullable=True)
    first_name: orm.Mapped[str]
    last_name: orm.Mapped[str]
    email: orm.Mapped[str]
    phone: orm.Mapped[str]
