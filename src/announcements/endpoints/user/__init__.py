from fastapi import APIRouter

from .announcements import router as announcements_router
from .filters import router as filters_router
from .favourite_announcements import router as favourite_announcements_router
from .promotions import router as promotions_router

router = APIRouter(prefix="/user")

router.include_router(announcements_router)
router.include_router(filters_router)
router.include_router(favourite_announcements_router)
router.include_router(promotions_router)
