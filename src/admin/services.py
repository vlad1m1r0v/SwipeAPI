from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.admin.models import Blacklist
from src.admin.repositories import BlacklistRepository


class BlacklistService(
    SQLAlchemyAsyncRepositoryService[Blacklist, BlacklistRepository]
):
    repository_type = BlacklistRepository
