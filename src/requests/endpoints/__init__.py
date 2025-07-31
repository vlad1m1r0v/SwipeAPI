from fastapi import APIRouter

from .builder import router as builder_router
from .user import router as user_router

router = APIRouter()

router.include_router(builder_router)
router.include_router(user_router)
