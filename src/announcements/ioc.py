from typing import AsyncIterator, Iterator

import dishka as di
from sqlalchemy.ext import asyncio as sa
from sqlalchemy.orm import Session

from src.announcements.services import (
    AnnouncementService,
    AnnouncementStatusChangeService,
    AnnouncementViewService,
    AnnouncementFilterService,
    AnnouncementPromotionService,
    AnnouncementFavouriteService,
    AnnouncementComplaintService,
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

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_announcement_complaint_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[AnnouncementComplaintService]:
        async with AnnouncementComplaintService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    def provide_announcement_status_change_service(
        self,
        session: Session,
    ) -> Iterator[AnnouncementStatusChangeService]:
        yield AnnouncementStatusChangeService(session=session)
