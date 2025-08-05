from src.auth.endpoints import router as auth_router
from src.user.endpoints import router as user_router
from src.admin.endpoints import router as admin_router
from src.builder.endpoints import router as builder_router
from src.buildings.endpoints import router as buildings_router
from src.apartments.endpoints import router as apartments_router
from src.notaries.endpoints import router as notaries_router
from src.requests.endpoints import router as requests_router
from src.announcements.endpoints import router as announcements_router

from fastapi import FastAPI


def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(admin_router)
    app.include_router(notaries_router)
    app.include_router(builder_router)
    app.include_router(apartments_router)
    app.include_router(buildings_router)
    app.include_router(requests_router)
    app.include_router(announcements_router)


__all__ = ["setup_routers"]
