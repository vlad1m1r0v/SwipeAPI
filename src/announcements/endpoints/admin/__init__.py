from fastapi import APIRouter

from .announcements import router as announcements_router
from .complaints import router as complaints_router

router = APIRouter(prefix="/admin")

router.include_router(announcements_router)
router.include_router(complaints_router)
