from fastapi import FastAPI

from src.core.setup.errors import setup_exception_handlers
from src.core.setup.containers import setup_containers
from src.core.setup.routers import setup_routers
from src.core.setup.files import mount_static


def setup(app: FastAPI) -> None:
    setup_exception_handlers(app)
    setup_containers(app)
    setup_routers(app)
    mount_static(app)


__all__ = ["setup"]
