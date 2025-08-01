from fastapi import APIRouter

from .complexes import router as complex_router

router = APIRouter()

router.include_router(complex_router)
