from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.core.constants import (
    MEDIA_FOLDER,
    MEDIA_DIR
)


def mount_static(app: FastAPI) -> None:
    app.mount(f"/{MEDIA_FOLDER}", StaticFiles(directory=MEDIA_DIR), name=MEDIA_FOLDER)
