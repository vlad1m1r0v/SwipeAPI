from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import FavouriteAnnouncement
from src.announcements.repositories import AnnouncementFavouriteRepository


class AnnouncementFavouriteService(
    SQLAlchemyAsyncRepositoryService[
        FavouriteAnnouncement, AnnouncementFavouriteRepository
    ]
):
    repository_type = AnnouncementFavouriteRepository

    async def get_favourite_user_announcements(
        self, user_id: int, limit: int, offset: int
    ) -> tuple[Sequence[FavouriteAnnouncement], int]:
        return await self.repository.get_favourite_user_announcements(
            user_id, limit, offset
        )

    async def get_favourite_user_announcement(
        self, favourite_announcement_id: int
    ) -> FavouriteAnnouncement:
        return await self.repository.get_favourite_user_announcement(
            favourite_announcement_id
        )
