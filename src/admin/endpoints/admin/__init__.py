from fastapi import APIRouter

from src.admin.endpoints.admin.blacklist import router as blacklist_router
from src.admin.endpoints.admin.profile import router as profile_router

router = APIRouter(prefix="/admin")

router.include_router(profile_router)
router.include_router(blacklist_router)

__all__ = ["router"]
