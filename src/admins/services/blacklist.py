from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.admins.models import Blacklist
from src.admins.repositories import BlacklistRepository


class BlacklistService(
    SQLAlchemyAsyncRepositoryService[Blacklist, BlacklistRepository]
):
    repository_type = BlacklistRepository
