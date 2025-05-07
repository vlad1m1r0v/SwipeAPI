from dishka import Provider, Scope, provide

from src.auth.services import AuthService


class AuthProvider(Provider):
    auth_service = provide(AuthService, scope=Scope.REQUEST)