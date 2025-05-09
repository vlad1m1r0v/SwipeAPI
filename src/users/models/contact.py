from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from .user import UserModel

class ContactModel(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    first_name: Mapped[str|None]
    last_name: Mapped[str|None]
    phone: Mapped[str]
    email: Mapped[str]

    user: Mapped["UserModel"] = relationship(back_populates="contact")