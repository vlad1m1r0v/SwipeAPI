from fastapi import APIRouter

from src.notaries.endpoints.admin import router as admin_router
from src.notaries.endpoints.shared import router as shared_router

router = APIRouter()

router.include_router(router=admin_router)
router.include_router(router=shared_router)

__all__ = ["router"]
