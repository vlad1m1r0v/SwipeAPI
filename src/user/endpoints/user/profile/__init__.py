from fastapi import APIRouter, Depends

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

from src.user.endpoints.user.profile.account import router as account_router
from src.user.endpoints.user.profile.contact import router as contact_router
from src.user.endpoints.user.profile.agent_contact import router as agent_contact_router
from src.user.endpoints.user.profile.subscription import router as subscription_router
from src.user.endpoints.user.profile.balance import router as balance_router
from src.user.endpoints.user.profile.notification_settings import (
    router as notification_settings_router,
)

router = APIRouter(prefix="/profile", tags=["User: Profile"])


@router.get(
    path="",
    response_model=SuccessResponse[GetUserSchema],
    responses=generate_examples(auth=True, user=True, role=True),
    response_model_exclude_none=True,
)
def get_profile(
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetUserSchema]:
    return SuccessResponse(data=user)


router.include_router(account_router)
router.include_router(contact_router)
router.include_router(agent_contact_router)
router.include_router(subscription_router)
router.include_router(balance_router)
router.include_router(notification_settings_router)

__all__ = ["router"]
