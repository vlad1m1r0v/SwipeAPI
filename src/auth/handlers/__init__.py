from fastapi import APIRouter

from src.auth.handlers.user import router as user_router

auth_router = APIRouter(prefix="/auth", tags=["auth"])

auth_router.include_router(user_router)