from src.user.endpoints.user import router as user_router
from src.user.endpoints.admin import router as admin_router

from fastapi import APIRouter

router = APIRouter()

router.include_router(user_router)
router.include_router(admin_router)

__all__ = ["router"]
