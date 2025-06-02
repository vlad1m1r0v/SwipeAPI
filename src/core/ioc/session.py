from typing import AsyncIterator

import dishka as di

from sqlalchemy.ext import asyncio as sa

from config import Config


class SessionProvider(di.Provider):
    @di.provide(scope=di.Scope.APP)
    def provide_engine(self, config: Config) -> sa.AsyncEngine:
        return sa.create_async_engine(config.db.url(is_async=True), echo=True)

    @di.provide(scope=di.Scope.APP)
    def provide_session_maker(
        self, engine: sa.AsyncEngine
    ) -> sa.async_sessionmaker[sa.AsyncSession]:
        return sa.async_sessionmaker(bind=engine, expire_on_commit=False)

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_session(
        self,
        session_maker: sa.async_sessionmaker[sa.AsyncSession],
    ) -> AsyncIterator[sa.AsyncSession]:
        async with session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
