from typing import AsyncIterator

import dishka as di

from sqlalchemy.ext import asyncio as sa

from src.buildings.services import (
    BlockService,
    SectionService,
    FloorService,
    RiserService,
    GridService,
)


class BuildingsProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_block_service(
        self, session: sa.AsyncSession
    ) -> AsyncIterator[BlockService]:
        async with BlockService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_section_service(
        self, session: sa.AsyncSession
    ) -> AsyncIterator[SectionService]:
        async with SectionService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_floor_service(
        self, session: sa.AsyncSession
    ) -> AsyncIterator[FloorService]:
        async with FloorService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_riser_service(
        self, session: sa.AsyncSession
    ) -> AsyncIterator[RiserService]:
        async with RiserService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_grid_service(
        self, session: sa.AsyncSession
    ) -> AsyncIterator[GridService]:
        yield GridService(session=session)
