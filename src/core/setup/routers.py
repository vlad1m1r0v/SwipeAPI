from src.auth.endpoints import router as auth_router
from src.users.endpoints import router as users_router

from fastapi import FastAPI


def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(users_router)

__all__ = ["setup_routers"]