from fastapi import APIRouter

from .profile import router as profile_router
from .account import router as account_router
from .advantages import router as advantages_router
from .infrastructure import router as infrastructure_router
from .formalization_and_payment_settings import (
    router as formalization_and_payment_settings_router,
)
from .news import router as news_router
from .document import router as document_router
from .gallery import router as gallery_router
from .blocks import router as blocks_router
from .sections import router as sections_router
from .floors import router as floors_router
from .risers import router as risers_router
from .add_to_complex_request import router as add_to_complex_request_router

router = APIRouter(prefix="/builder")

router.include_router(profile_router)
router.include_router(account_router)
router.include_router(advantages_router)
router.include_router(infrastructure_router)
router.include_router(formalization_and_payment_settings_router)
router.include_router(news_router)
router.include_router(document_router)
router.include_router(gallery_router)
router.include_router(blocks_router)
router.include_router(sections_router)
router.include_router(floors_router)
router.include_router(risers_router)
router.include_router(add_to_complex_request_router)
