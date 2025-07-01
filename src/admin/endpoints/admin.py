from fastapi import APIRouter

from src.admin.endpoints.blacklist import router as blacklist_router
from src.admin.endpoints.notaries import router as notaries_router
from src.admin.endpoints.profile import router as profile_router

router = APIRouter(prefix="/admin")

router.include_router(profile_router)
router.include_router(blacklist_router)
router.include_router(notaries_router)
