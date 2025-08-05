from fastapi import APIRouter

from .user import router as user_router
from .shared import router as shared_router

router = APIRouter()

router.include_router(user_router)
router.include_router(shared_router)
