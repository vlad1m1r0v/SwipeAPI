from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from .user import UserModel

class AgentContactModel(Base):
    __tablename__ = "agent_contacts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    phone: Mapped[str | None]
    email: Mapped[str | None]

    user: Mapped["UserModel"] = relationship(back_populates="agent_contact")