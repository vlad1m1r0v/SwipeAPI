from fastapi import APIRouter

from .builder import router as builder_router
from .shared import router as shared_router
from .user import router as favourite_complexes_router

router = APIRouter()

router.include_router(builder_router)
router.include_router(shared_router)
router.include_router(favourite_complexes_router)
