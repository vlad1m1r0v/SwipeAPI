from fastapi import APIRouter

from src.user.endpoints.user.profile import router as profile_router

router = APIRouter(prefix="/user")

router.include_router(profile_router)

__all__ = ["router"]
