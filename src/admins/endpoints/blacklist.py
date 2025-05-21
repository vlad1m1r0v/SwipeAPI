from fastapi import (
    APIRouter,
    Form,
    Query,
    Depends,
)

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from advanced_alchemy.service import OffsetPagination

from src.core.schemas import (
    SuccessfulMessageSchema
)

from src.admins.schemas import GetAdminSchema
from src.admins.services import BlacklistService

from src.users.schemas import GetUserAccountSchema
from src.users.services import UserService

from src.auth.dependencies import admin_from_token

router = APIRouter(prefix="/blacklist")


@router.get("", response_model=OffsetPagination[GetUserAccountSchema])
@inject
async def get_blacklist(
        user_service: FromDishka[UserService],
        limit: int = Query(default=20),
        offset: int = Query(default=0),
        search: str = Query(default=""),

        _: GetAdminSchema = Depends(admin_from_token)

) -> OffsetPagination[GetUserAccountSchema]:
    results, total = await user_service.get_blacklisted_users(
        limit=limit,
        offset=offset,
        search=search
    )
    return user_service.to_schema(results, total, schema_type=GetUserAccountSchema)


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
