from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query, Body
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.user.schemas import GetUserSchema

from src.core.exceptions import (
    IntegrityErrorException,
    IsNotOwnerException,
    NotFoundException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.requests.services import AddToComplexRequestService
from src.requests.schemas import (
    GetAddToComplexRequestUserSchema,
    CreateAddToComplexRequest,
)
from src.requests.dependencies import check_user_owns_request

from src.auth.dependencies import user_from_token

router = APIRouter(prefix="/user/requests", tags=["User: Requests"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetAddToComplexRequestUserSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_requests_for_user(
    add_to_complex_request_service: FromDishka[AddToComplexRequestService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetAddToComplexRequestUserSchema]]:
    results, total = await add_to_complex_request_service.get_requests_for_user(
        limit=limit, offset=offset, user_id=user.id
    )
    return SuccessResponse(
        data=add_to_complex_request_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit, offset)],
            schema_type=GetAddToComplexRequestUserSchema,
        )
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        IntegrityErrorException, auth=True, role=True, user=True
    ),
    response_model=SuccessResponse[GetAddToComplexRequestUserSchema],
)
@inject
async def create_add_to_complex_request(
    add_to_complex_request_service: FromDishka[AddToComplexRequestService],
    data: CreateAddToComplexRequest = Body(),
    _: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetAddToComplexRequestUserSchema]:
    created = await add_to_complex_request_service.create(data=data.model_dump())
    request = await add_to_complex_request_service.get_user_request(created.id)
    return SuccessResponse(
        data=add_to_complex_request_service.to_schema(
            data=request, schema_type=GetAddToComplexRequestUserSchema
        )
    )


@router.delete(
    path="/{request_id}",
    response_model=SuccessResponse,
    responses=generate_examples(
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
        user=True,
    ),
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_apartment(
    request_service: FromDishka[AddToComplexRequestService],
    request_id: int,
    _: GetUserSchema = Depends(check_user_owns_request),
):
    await request_service.delete(item_id=request_id)
    return SuccessResponse(message="Request has been deleted successfully.")
