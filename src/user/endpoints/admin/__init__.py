from fastapi import APIRouter

from src.user.endpoints.admin.users import router as users_router

router = APIRouter(prefix="/admin")

router.include_router(users_router)

__all__ = ["router"]
