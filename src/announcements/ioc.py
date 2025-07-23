from typing import AsyncIterator

import dishka as di
from sqlalchemy.ext import asyncio as sa

from src.announcements.services import (
    AnnouncementService,
    AnnouncementViewService,
    AnnouncementFilterService,
    AnnouncementPromotionService,
    AnnouncementFavouriteService,
)


class AnnouncementsProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_announcement_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[AnnouncementService]:
        async with AnnouncementService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_announcement_view_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[AnnouncementViewService]:
        async with AnnouncementViewService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_announcement_filter_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[AnnouncementFilterService]:
        async with AnnouncementFilterService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_announcement_promotion_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[AnnouncementPromotionService]:
        async with AnnouncementPromotionService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_announcement_favourite_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[AnnouncementFavouriteService]:
        async with AnnouncementFavouriteService.new(session=session) as service:
            yield service
