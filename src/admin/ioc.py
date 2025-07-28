from typing import AsyncIterator

import dishka as di
from sqlalchemy.ext import asyncio as sa

from src.admin.services import BlacklistService


class AdminProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_blacklist_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[BlacklistService]:
        async with BlacklistService.new(session=session) as service:
            yield service
