from typing import AsyncIterator

import dishka as di

from redis.asyncio import Redis

from config import Config


class RedisProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_redis(self, config: Config) -> AsyncIterator[Redis]:
        redis = Redis.from_url(config.redis.redis_storage_url)
        yield redis
        await redis.close()
