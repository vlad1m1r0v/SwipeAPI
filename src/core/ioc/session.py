from typing import AsyncIterator, Iterator

import dishka as di

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from sqlalchemy.ext import asyncio as sa

from config import Config


class SessionProvider(di.Provider):
    @di.provide(scope=di.Scope.APP)
    def provide_async_engine(self, config: Config) -> sa.AsyncEngine:
        return sa.create_async_engine(config.db.url(is_async=True), echo=True)

    @di.provide(scope=di.Scope.APP)
    def provide_async_session_maker(
        self, engine: sa.AsyncEngine
    ) -> sa.async_sessionmaker[sa.AsyncSession]:
        return sa.async_sessionmaker(bind=engine, expire_on_commit=False)

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_async_session(
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

    @di.provide(scope=di.Scope.APP)
    def provide_sync_engine(self, config: Config) -> Engine:
        return create_engine(config.db.url(is_async=False), echo=True)

    @di.provide(scope=di.Scope.APP)
    def provide_sync_session_maker(self, sync_engine: Engine) -> sessionmaker:
        return sessionmaker(bind=sync_engine, expire_on_commit=False)

    @di.provide(scope=di.Scope.REQUEST)
    def provide_sync_session(
        self, sync_session_maker: sessionmaker
    ) -> Iterator[Session]:
        with sync_session_maker() as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
