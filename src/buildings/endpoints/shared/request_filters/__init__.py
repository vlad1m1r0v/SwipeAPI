from fastapi import APIRouter

from .complexes import router as complex_router
from .blocks import router as blocks_router
from .sections import router as sections_router
from .floors import router as floors_router
from .risers import router as risers_router

router = APIRouter(prefix="/request-filters", tags=["Shared: Request Filters"])

router.include_router(complex_router)
router.include_router(blocks_router)
router.include_router(sections_router)
router.include_router(floors_router)
router.include_router(risers_router)
