from typing import AsyncIterator

import dishka as di

from redis.asyncio import Redis

from config import Config


class InMemoryDBProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_in_memory_db_connection(
        self, config: Config
    ) -> AsyncIterator[Redis]:
        redis = Redis.from_url(config.in_memory_db.url)
        yield redis
        await redis.close()
