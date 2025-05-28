from fastapi import FastAPI

from src.core.setup.server.errors import setup_exception_handlers
from src.core.setup.server.containers import setup_containers
from src.core.setup.server.routers import setup_routers
from src.core.setup.server.files import mount_static


def setup(app: FastAPI) -> None:
    setup_exception_handlers(app)
    setup_containers(app)
    setup_routers(app)
    mount_static(app)


__all__ = ["setup"]
