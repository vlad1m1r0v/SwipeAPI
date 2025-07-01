from advanced_alchemy.base import BigIntAuditBase

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import orm
import sqlalchemy as sa


class Notary(BigIntAuditBase):
    photo = sa.Column(JSONB)
    first_name: orm.Mapped[str]
    last_name: orm.Mapped[str]
    email: orm.Mapped[str]
    phone: orm.Mapped[str]
