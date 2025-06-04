from src.auth.endpoints import router as auth_router
from src.users.endpoints import router as users_router
from src.admins.endpoints import router as admins_router
from src.builders.endpoints import router as builders_router

from fastapi import FastAPI


def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(admins_router)
    app.include_router(builders_router)


__all__ = ["setup_routers"]
