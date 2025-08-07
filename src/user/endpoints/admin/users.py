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

from src.admin.schemas import GetAdminSchema

from src.user.schemas import GetUserAccountSchema
from src.user.services import UserService

from src.auth.dependencies import admin_from_token

router = APIRouter(prefix="/users", tags=["Admin: Users"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetUserAccountSchema]],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_users(
    user_service: FromDishka[UserService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    search: str = Query(default=""),
    _: GetAdminSchema = Depends(admin_from_token),
) -> SuccessResponse[OffsetPagination[GetUserAccountSchema]]:
    results, total = await user_service.get_users(
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
