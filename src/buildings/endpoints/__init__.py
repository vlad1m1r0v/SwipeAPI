from fastapi import APIRouter

from .shared import router as shared_router

router = APIRouter()

router.include_router(shared_router)
