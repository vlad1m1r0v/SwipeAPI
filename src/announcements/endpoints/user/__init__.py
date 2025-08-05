from fastapi import APIRouter

from .announcements import router as announcements_router

router = APIRouter(prefix="/user")

router.include_router(announcements_router)
