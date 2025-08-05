from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import Filter
from src.announcements.repositories import AnnouncementFilterRepository


class AnnouncementFilterService(
    SQLAlchemyAsyncRepositoryService[Filter, AnnouncementFilterRepository]
):
    repository_type = AnnouncementFilterRepository

    async def create_filter(self, user_id: int, data: dict) -> Filter:
        return await self.repository.create_filter(user_id, data)

    async def get_user_filters(
        self, user_id: int, limit: int, offset: int
    ) -> tuple[Sequence[Filter], int]:
        return await self.repository.get_user_filters(user_id, limit, offset)
