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

router = APIRouter(prefix="/builders", tags=["builders"])

router.include_router(profile_router)
router.include_router(account_router)
router.include_router(advantages_router)
router.include_router(infrastructure_router)
router.include_router(formalization_and_payment_settings_router)
router.include_router(news_router)
router.include_router(document_router)
