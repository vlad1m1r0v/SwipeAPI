from fastapi import APIRouter

from .builder import router as builder_router

router = APIRouter()

router.include_router(builder_router)
