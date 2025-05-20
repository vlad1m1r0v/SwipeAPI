from fastapi import APIRouter

from src.admins.endpoints.blacklist import router as blacklist_router

router = APIRouter(prefix="/admins", tags=["admins"])

router.include_router(blacklist_router)