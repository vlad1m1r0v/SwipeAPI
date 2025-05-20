from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.admins import models as m
from src.admins import repositories as r


class NotaryService(SQLAlchemyAsyncRepositoryService[m.Notary, r.NotaryRepository]):
    repository_type = r.NotaryRepository

class BlacklistService(SQLAlchemyAsyncRepositoryService[m.Blacklist, r.BlacklistRepository]):
    repository_type = r.BlacklistRepository

__all__ = [
    "NotaryService",
    "BlacklistService"
]
