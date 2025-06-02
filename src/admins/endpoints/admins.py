from fastapi import APIRouter

from src.admins.endpoints.blacklist import router as blacklist_router
from src.admins.endpoints.notaries import router as notaries_router
from src.admins.endpoints.profile import router as profile_router

router = APIRouter(prefix="/admins", tags=["admins"])

router.include_router(blacklist_router)
router.include_router(notaries_router)
router.include_router(profile_router)
