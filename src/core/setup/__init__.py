from fastapi import FastAPI

from src.core.setup.storage import setup_file_storage
from src.core.setup.errors import setup_exception_handlers
from src.core.setup.containers import setup_containers
from src.core.setup.routers import setup_routers


def setup(app: FastAPI) -> None:
    setup_file_storage()
    setup_exception_handlers(app)
    setup_containers(app)
    setup_routers(app)


__all__ = ["setup"]
