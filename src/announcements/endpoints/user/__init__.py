from fastapi import APIRouter

from .announcements import router as announcements_router
from .filters import router as filters_router

router = APIRouter(prefix="/user")

router.include_router(announcements_router)
router.include_router(filters_router)
