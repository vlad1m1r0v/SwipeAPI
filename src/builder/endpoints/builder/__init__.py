from fastapi import APIRouter

from .profile import router as profile_router

router = APIRouter(prefix="/builder")

router.include_router(profile_router)
