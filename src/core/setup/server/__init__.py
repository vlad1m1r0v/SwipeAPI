from fastapi import FastAPI

from src.core.setup.server.errors import setup_exception_handlers
from src.core.setup.server.containers import setup_containers
from src.core.setup.server.routers import setup_routers
from src.core.setup.server.files import mount_static
from src.core.setup.server.autoclean import setup_autoclean


def setup(app: FastAPI) -> None:
    setup_exception_handlers(app)
    setup_containers(app)
    setup_routers(app)
    setup_autoclean()
    mount_static(app)


__all__ = ["setup"]
