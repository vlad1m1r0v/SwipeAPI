from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from advanced_alchemy.filters import (
    LimitOffset,
    SearchFilter,
)

from src.admins import models as m
from src.admins import repositories as r


class NotaryService(SQLAlchemyAsyncRepositoryService[m.Notary, r.NotaryRepository]):
    repository_type = r.NotaryRepository

    async def get_notaries(self, limit: int, offset: int, search: str) -> tuple[Sequence[m.Notary], int]:
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


class BlacklistService(SQLAlchemyAsyncRepositoryService[m.Blacklist, r.BlacklistRepository]):
    repository_type = r.BlacklistRepository


__all__ = [
    "NotaryService",
    "BlacklistService"
]
