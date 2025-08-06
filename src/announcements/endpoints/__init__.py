from fastapi import APIRouter

from .user import router as user_router
from .shared import router as shared_router
from .admin import router as admin_router

router = APIRouter()

router.include_router(user_router)
router.include_router(shared_router)
router.include_router(admin_router)
