from fastapi import APIRouter

from .grid import router as grid_router
from .request_filters import router as request_filters_router

router = APIRouter()

router.include_router(grid_router)
router.include_router(request_filters_router)
