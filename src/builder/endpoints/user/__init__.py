from fastapi import APIRouter

from .favourite_complexes import router as favourite_complexes_router

router = APIRouter()

router.include_router(favourite_complexes_router)
