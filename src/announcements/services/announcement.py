from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.enums import (
    Type,
    Status,
    PropertyType,
    BillingOptions,
)

from src.apartments.enums import Rooms, Finishing

from src.announcements.models import Announcement
from src.announcements.repositories import AnnouncementRepository


class AnnouncementService(
    SQLAlchemyAsyncRepositoryService[Announcement, AnnouncementRepository]
):
    repository_type = AnnouncementRepository

    async def create_announcement(self, data: dict) -> Announcement:
        return await self.repository.create_announcement(data)

    async def get_announcements_for_shared(
        self,
        limit: int,
        offset: int,
        filter_id: int | None,
        district: str | None,
        neighbourhood: str | None,
        price_min: int | None,
        price_max: int | None,
        area_min: float | None,
        area_max: float | None,
        rooms: Rooms | None,
        finishing: Finishing | None,
        complex_type: Type | None,
        status: Status | None,
        property_type: PropertyType | None,
        billing_options: BillingOptions | None,
    ) -> tuple[Sequence[Announcement], int]:
        return await self.repository.get_announcements_for_shared(
            limit,
            offset,
            filter_id,
            district,
            neighbourhood,
            price_min,
            price_max,
            area_min,
            area_max,
            rooms,
            finishing,
            complex_type,
            status,
            property_type,
            billing_options,
        )

    async def get_announcements_for_user(
        self, user_id: int, limit: int, offset: int
    ) -> tuple[Sequence[Announcement], int]:
        return await self.repository.get_announcements_for_user(user_id, limit, offset)

    async def get_announcements_for_admin(
        self, limit: int, offset: int
    ) -> tuple[Sequence[Announcement], int]:
        return await self.repository.get_announcements_for_admin(limit, offset)

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
