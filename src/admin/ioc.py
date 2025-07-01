from typing import AsyncIterator

import dishka as di
from sqlalchemy.ext import asyncio as sa

from src.admin.services import NotaryService, BlacklistService


class AdminProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_notary_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[NotaryService]:
        async with NotaryService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_blacklist_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[BlacklistService]:
        async with BlacklistService.new(session=session) as service:
            yield service
