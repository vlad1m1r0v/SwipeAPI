from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.admin.models import Notary
from src.admin.repositories import NotaryRepository


class NotaryService(SQLAlchemyAsyncRepositoryService[Notary, NotaryRepository]):
    repository_type = NotaryRepository

    async def get_notaries(
        self, limit: int, offset: int, search: str
    ) -> tuple[Sequence[Notary], int]:
        return await self.repository.get_notaries(limit, offset, search)
