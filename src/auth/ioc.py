from typing import Iterator

from config import Config

import dishka as di

from redis.asyncio import Redis

from src.auth.services import AuthService, SignService, JwtService

from src.user.services import UserService, SubscriptionService

from src.admin.services import BlacklistService


class AuthProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    def provide_jwt_service(
        self,
        config: Config,
    ) -> Iterator[JwtService]:
        yield JwtService(config=config)

    @di.provide(scope=di.Scope.REQUEST)
    def provide_sign_service(
        self,
        config: Config,
        redis: Redis,
    ) -> Iterator[SignService]:
        yield SignService(config=config, redis=redis)

    @di.provide(scope=di.Scope.REQUEST)
    def provide_auth_service(
        self,
        jwt_service: JwtService,
        sign_service: SignService,
        user_service: UserService,
        blacklist_service: BlacklistService,
        subscription_service: SubscriptionService,
    ) -> Iterator[AuthService]:
        yield AuthService(
            jwt_service=jwt_service,
            sign_service=sign_service,
            user_service=user_service,
            blacklist_service=blacklist_service,
            subscription_service=subscription_service,
        )


__all__ = ["AuthProvider"]
