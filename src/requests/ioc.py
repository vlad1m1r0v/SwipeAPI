from typing import AsyncIterator

import dishka as di

from sqlalchemy.ext import asyncio as sa

from src.requests.services import AddToComplexRequestService


class RequestsProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_add_to_complex_request_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[AddToComplexRequestService]:
        async with AddToComplexRequestService.new(session=session) as service:
            yield service
