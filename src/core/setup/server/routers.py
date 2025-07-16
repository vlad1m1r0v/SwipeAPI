from src.auth.endpoints import router as auth_router
from src.user.endpoints import router as user_router
from src.admin.endpoints import admin_router, notaries_router
from src.builder.endpoints import (
    builder_router,
    complexes_router,
    blocks_router,
    sections_router,
    floors_router,
    risers_router,
)
from src.apartments.endpoints import router as apartments_router

from fastapi import FastAPI


def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)

    app.include_router(user_router)

    app.include_router(admin_router)
    app.include_router(notaries_router)

    app.include_router(builder_router)
    app.include_router(complexes_router)
    app.include_router(blocks_router)
    app.include_router(sections_router)
    app.include_router(floors_router)
    app.include_router(risers_router)

    app.include_router(apartments_router)


__all__ = ["setup_routers"]
