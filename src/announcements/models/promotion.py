from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import orm
import sqlalchemy as sa

from advanced_alchemy.base import BigIntAuditBase

from src.announcements.enums import Colour, Phrase

if TYPE_CHECKING:
    from src.announcements.models import Announcement


class Promotion(BigIntAuditBase):
    __tablename__ = "promotions"

    announcement_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("announcements.id", ondelete="CASCADE"),
    )

    highlight_colour: Colour = sa.Column(sa.Enum(Colour), nullable=True)
    highlight_expiry_date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        nullable=True,
    )

    phrase: Phrase = sa.Column(sa.Enum(Phrase), nullable=True)
    phrase_expiry_date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        nullable=True,
    )

    big_advert_expiry_date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        nullable=True,
    )

    boost_expiry_date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, nullable=True
    )

    announcement: orm.Mapped["Announcement"] = orm.relationship(
        back_populates="promotion"
    )
