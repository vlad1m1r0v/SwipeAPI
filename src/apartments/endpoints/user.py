from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query, Body
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.exceptions import (
    NotFoundException,
    IntegrityErrorException,
    IsNotOwnerException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.apartments.schemas import (
    GetApartmentUserListSchema,
    GetApartmentUserDetail,
    CreateApartmentSchema,
    UpdateApartmentSchema,
)
from src.apartments.services import ApartmentService
from src.apartments.dependencies import check_user_owns_apartment

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

router = APIRouter(prefix="/user/apartments", tags=["User: Apartments"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetApartmentUserListSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_apartments(
    apartment_service: FromDishka[ApartmentService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetApartmentUserListSchema]]:
    results, total = await apartment_service.get_apartments_list_for_user(
        limit=limit, offset=offset, user_id=user.id
    )
    return SuccessResponse(
        data=apartment_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetApartmentUserListSchema,
        )
    )


@router.get(
    path="/{apartment_id}",
    response_model=SuccessResponse[GetApartmentUserDetail],
    responses=generate_examples(NotFoundException, auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_apartment(
    apartment_service: FromDishka[ApartmentService],
    apartment_id: int,
    _: GetUserSchema = Depends(check_user_owns_apartment),
) -> SuccessResponse[GetApartmentUserDetail]:
    apartment = await apartment_service.get_apartment_detail_for_user(apartment_id)
    return SuccessResponse(
        data=apartment_service.to_schema(
            data=apartment, schema_type=GetApartmentUserDetail
        )
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        IntegrityErrorException, auth=True, role=True, user=True
    ),
    response_model=SuccessResponse[GetApartmentUserDetail],
)
@inject
async def create_apartment(
    apartment_service: FromDishka[ApartmentService],
    data: CreateApartmentSchema = Body(),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetApartmentUserDetail]:
    apartment = await apartment_service.create_apartment(user_id=user.id, data=data)
    return SuccessResponse(
        data=apartment_service.to_schema(
            data=apartment, schema_type=GetApartmentUserDetail
        )
    )


@router.patch(
    path="/{apartment_id}",
    status_code=status.HTTP_200_OK,
    responses=generate_examples(
        IntegrityErrorException, auth=True, role=True, user=True
    ),
    response_model=SuccessResponse[GetApartmentUserDetail],
)
@inject
async def update_apartment(
    apartment_id: int,
    apartment_service: FromDishka[ApartmentService],
    data: UpdateApartmentSchema = Body(),
    _: GetUserSchema = Depends(check_user_owns_apartment),
) -> SuccessResponse[GetApartmentUserDetail]:
    apartment = await apartment_service.update_apartment(
        item_id=apartment_id, data=data
    )
    return SuccessResponse(
        data=apartment_service.to_schema(
            data=apartment, schema_type=GetApartmentUserDetail
        )
    )


@router.delete(
    path="/{apartment_id}",
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
    apartment_service: FromDishka[ApartmentService],
    apartment_id: int,
    _: GetUserSchema = Depends(check_user_owns_apartment),
):
    await apartment_service.delete(item_id=apartment_id)
    return SuccessResponse(message="Apartment has been deleted successfully.")
