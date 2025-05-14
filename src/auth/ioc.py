from typing import Iterator

from config import Config

import dishka as di

from src.auth import services as s


class AuthProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    def provide_jwt_service(
            self,
            config: Config,
    ) -> Iterator[s.JwtService]:
        yield s.JwtService(config=config)

__all__ = ["AuthProvider"]