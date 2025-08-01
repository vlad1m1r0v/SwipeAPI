from typing import AsyncIterator

import dishka as di

from sqlalchemy.ext import asyncio as sa

from src.apartments.services import ApartmentService, ApartmentGalleryService


class ApartmentsProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_apartment_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[ApartmentService]:
        async with ApartmentService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_apartment_gallery_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[ApartmentGalleryService]:
        async with ApartmentGalleryService.new(session=session) as service:
            yield service
