from fastapi import APIRouter

from src.auth.endpoints.user import router as user_router
from src.auth.endpoints.admin import router as admin_router
from src.auth.endpoints.builder import router as builder_router
from src.auth.endpoints.common import router as common_router

router = APIRouter(prefix="/auth")

router.include_router(user_router)
router.include_router(admin_router)
router.include_router(builder_router)
router.include_router(common_router)

__all__ = ["router"]
