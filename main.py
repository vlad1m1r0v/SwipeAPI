import uvicorn

from advanced_alchemy.types.file_object import storages
from advanced_alchemy.types.file_object.backends.obstore import ObstoreBackend

import dishka as di
from dishka.integrations.fastapi import setup_dishka

from config import Config, config

from src.core.errors import setup_error_handlers

from src.core.ioc import ConfigProvider, SessionProvider
from src.auth.ioc import AuthProvider
from src.users.ioc import UsersProvider

from src.auth.endpoints import router as auth_router

from fastapi import FastAPI


def setup_containers(app: FastAPI) -> None:
    container = di.make_async_container(
        ConfigProvider(),
        SessionProvider(),
        AuthProvider(),
        UsersProvider(),
        context={Config: config},
    )

    setup_dishka(container, app)


def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)


def setup_file_storage() -> None:
    from pathlib import Path

    storages.register_backend(ObstoreBackend(
        key="local",
        fs=f"file:///{Path(__file__).parent}/uploads",
    ))


def setup(app: FastAPI) -> None:
    setup_file_storage()
    setup_error_handlers(app)
    setup_containers(app)
    setup_routers(app)


server = FastAPI()
setup(server)

if __name__ == "__main__":
    uvicorn.run("main:server", reload=True)
