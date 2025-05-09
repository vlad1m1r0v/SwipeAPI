from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, BigInteger, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.users.models import UserModel

DEFAULT_BALANCE = Decimal("5000.00")

class BalanceModel(Base):
    __tablename__ = "balances"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    value: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2), default=DEFAULT_BALANCE)

    user: Mapped["UserModel"] = relationship(back_populates="balance")
