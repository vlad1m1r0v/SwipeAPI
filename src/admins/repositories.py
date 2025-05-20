from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.admins import models as m


class NotaryRepository(SQLAlchemyAsyncRepository[m.Notary]):
    model_type = m.Notary


class BlacklistRepository(SQLAlchemyAsyncRepository[m.Blacklist]):
    model_type = m.Blacklist


__all__ = [
    "NotaryRepository",
    "BlacklistRepository"
]
