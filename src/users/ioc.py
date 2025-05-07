from typing import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.services import UserService


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_user_service(
        self,
        session: AsyncSession,
    ) -> AsyncIterator[UserService]:
        async with UserService.new(session=session) as service:
            yield service