from typing import AsyncIterator

import dishka as di

from sqlalchemy.ext import asyncio as sa

from src.builders.services import (
    ComplexService,
    InfrastructureService,
    AdvantagesService,
    FormalizationAndPaymentSettingsService,
    NewsService,
    DocumentService,
    GalleryService,
    BlockService,
)


class BuilderProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_complex_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[ComplexService]:
        async with ComplexService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_infrastructure_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[InfrastructureService]:
        async with InfrastructureService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_advantages_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[AdvantagesService]:
        async with AdvantagesService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_formalization_and_payment_settings_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[FormalizationAndPaymentSettingsService]:
        async with FormalizationAndPaymentSettingsService.new(
            session=session
        ) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_news_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[NewsService]:
        async with NewsService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_document_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[DocumentService]:
        async with DocumentService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_gallery_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[GalleryService]:
        async with GalleryService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_block_service(
        self, session: sa.AsyncSession
    ) -> AsyncIterator[BlockService]:
        async with BlockService.new(session=session) as service:
            yield service
