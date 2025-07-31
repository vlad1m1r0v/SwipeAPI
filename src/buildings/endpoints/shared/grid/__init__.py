from fastapi import APIRouter

from .sections import router as section_router
from .layout import router as layout_router
from .apartments import router as apartment_router

router = APIRouter(prefix="/grid", tags=["Shared: Apartment Grid"])

router.include_router(section_router)
router.include_router(layout_router)
router.include_router(apartment_router)
