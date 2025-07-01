from fastapi import APIRouter

from .profile import router as profile_router
from .account import router as account_router
from .contact import router as contact_router
from .agent_contact import router as agent_contact_router
from .subscription import router as subscription_router
from .balance import router as balance_router
from .notification_settings import router as notification_settings_router

router = APIRouter(prefix="/user")

router.include_router(profile_router)
router.include_router(account_router)
router.include_router(contact_router)
router.include_router(agent_contact_router)
router.include_router(subscription_router)
router.include_router(balance_router)
router.include_router(notification_settings_router)
