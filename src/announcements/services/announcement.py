from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import Announcement
from src.announcements.repositories import AnnouncementRepository


class AnnouncementService(
    SQLAlchemyAsyncRepositoryService[Announcement, AnnouncementRepository]
):
    repository_type = AnnouncementRepository

    async def create_announcement(self, data: dict) -> Announcement:
        return await self.repository.create_announcement(data)

    async def get_announcements_for_user(
        self, user_id: int, limit: int, offset: int
    ) -> tuple[Sequence[Announcement], int]:
        return await self.repository.get_announcements_for_user(user_id, limit, offset)

    async def get_announcement_detail_for_shared(
        self, user_id: int, announcement_id: int
    ) -> Announcement:
        return await self.repository.get_announcement_detail_for_shared(
            user_id, announcement_id
        )

    async def get_announcement_detail_for_user(
        self, announcement_id: int
    ) -> Announcement:
        return await self.repository.get_announcement_detail_for_user(announcement_id)
