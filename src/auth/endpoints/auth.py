from fastapi import APIRouter

from src.auth.endpoints.users import router as user_router

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(user_router)