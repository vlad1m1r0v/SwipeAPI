from fastapi import (
    APIRouter,
    Query,
    Depends,
)
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse
from src.core.exceptions import (
    IntegrityErrorException,
    DuplicateKeyException,
    NotFoundException,
)

from src.admin.schemas import GetAdminSchema, BlacklistUserSchema
from src.admin.services import BlacklistService

from src.user.schemas import GetUserAccountSchema
from src.user.services import UserService

from src.auth.dependencies import admin_from_token

router = APIRouter(prefix="/blacklist", tags=["Admin: Blacklist"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetUserAccountSchema]],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_blacklist(
    user_service: FromDishka[UserService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    search: str = Query(default=""),
    _: GetAdminSchema = Depends(admin_from_token),
) -> SuccessResponse[OffsetPagination[GetUserAccountSchema]]:
    results, total = await user_service.get_blacklisted_users(
        limit=limit, offset=offset, search=search
    )
    return SuccessResponse(
        data=user_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetUserAccountSchema,
        )
    )


@router.post(
    path="",
    response_model=SuccessResponse,
    responses=generate_examples(
        IntegrityErrorException, DuplicateKeyException, auth=True, role=True
    ),
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
@inject
async def blacklist_user(
    blacklist_service: FromDishka[BlacklistService],
    data: BlacklistUserSchema,
    _: GetAdminSchema = Depends(admin_from_token),
) -> SuccessResponse:
    await blacklist_service.create(data={"user_id": data.user_id})
    return SuccessResponse(message="User has been blacklisted.")


@router.delete(
    path="/{record_id}",
    response_model=SuccessResponse,
    responses=generate_examples(NotFoundException, auth=True, role=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def remove_user_from_blacklist(
    blacklist_service: FromDishka[BlacklistService],
    record_id: int,
    _: GetAdminSchema = Depends(admin_from_token),
):
    await blacklist_service.delete(item_id=record_id)
    return SuccessResponse(
        message="User has been removed from blacklist.",
    )
