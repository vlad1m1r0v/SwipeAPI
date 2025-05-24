from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from advanced_alchemy.filters import (
    LimitOffset,
    SearchFilter,
)

from src.admins.models import Notary
from src.admins.repositories import NotaryRepository


class NotaryService(SQLAlchemyAsyncRepositoryService[Notary, NotaryRepository]):
    repository_type = NotaryRepository

    async def get_notaries(self, limit: int, offset: int, search: str) -> tuple[Sequence[Notary], int]:
        limit_offset = LimitOffset(limit=limit, offset=offset)
        search_filter = SearchFilter(
            field_name={'name', 'email', 'phone'},
            value=search,
            ignore_case=True,
        )

        results, total = await self.list_and_count(
            limit_offset,
            search_filter,
        )

        return results, total