from fastapi import (
    APIRouter,
    Form,
    Depends
)

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.core.schemas import (
    SuccessfulMessageSchema
)

from src.admins.schemas import GetAdminSchema
from src.admins.services import BlacklistService

from src.auth.dependencies import admin_from_token

router = APIRouter(prefix="/blacklist")


@router.post("", response_model=SuccessfulMessageSchema)
@inject
async def blacklist_user(
        blacklist_service: FromDishka[BlacklistService],
        user_id: int = Form(),
        _: GetAdminSchema = Depends(admin_from_token)
):
    await blacklist_service.create(data={'user_id': user_id})
    return SuccessfulMessageSchema(
        message="User has been blacklisted.",
    )


@router.delete("/{record_id}", response_model=SuccessfulMessageSchema)
@inject
async def remove_user_from_blacklist(
        blacklist_service: FromDishka[BlacklistService],
        record_id: int,
        _: GetAdminSchema = Depends(admin_from_token)
):
    await blacklist_service.delete(item_id=record_id)
    return SuccessfulMessageSchema(
        message="User has been removed from blacklist.",
    )
