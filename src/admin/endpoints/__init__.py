from fastapi import APIRouter

from src.admin.endpoints.admin import router as admin_router

router = APIRouter()

router.include_router(admin_router)

__all__ = ["router"]
