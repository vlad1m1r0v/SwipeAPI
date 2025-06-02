import dishka as di

from config import Config


class ConfigProvider(di.Provider):
    config = di.from_context(provides=Config, scope=di.Scope.APP)
