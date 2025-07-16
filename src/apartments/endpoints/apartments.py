from fastapi import APIRouter

from .user import router as user_router
from .add_to_complex_request import router as add_to_complex_request_router

router = APIRouter()

router.include_router(user_router)
router.include_router(add_to_complex_request_router)
