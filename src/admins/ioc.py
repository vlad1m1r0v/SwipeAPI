from typing import AsyncIterator

import dishka as di
from sqlalchemy.ext import asyncio as sa

from src.admins import services as s


class AdminsProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_notary_service(
            self,
            session: sa.AsyncSession,
    ) -> AsyncIterator[s.NotaryService]:
        async with s.NotaryService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_blacklist_service(
            self,
            session: sa.AsyncSession,
    ) -> AsyncIterator[s.BlacklistService]:
        async with s.BlacklistService.new(session=session) as service:
            yield service
