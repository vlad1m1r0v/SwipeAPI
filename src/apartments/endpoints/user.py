from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Request, Depends, Body
from starlette import status


from src.core.exceptions import (
    IsNotOwnerException,
    IntegrityErrorException,
    NotFoundException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.apartments.schemas import GetApartmentDetailsSchema, CreateApartmentSchema
from src.apartments.services import ApartmentService
from src.apartments.dependencies import check_user_owns_apartment

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

router = APIRouter(prefix="/user/apartments", tags=["User: Apartments"])


@router.get(
    path="/{apartment_id}",
    response_model=SuccessResponse[GetApartmentDetailsSchema],
    responses=generate_examples(NotFoundException, auth=True, role=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_apartment(
    apartment_service: FromDishka[ApartmentService],
    apartment_id: int,
    _: GetUserSchema = Depends(check_user_owns_apartment),
) -> SuccessResponse[GetApartmentDetailsSchema]:
    apartment = await apartment_service.get_apartment_details(apartment_id)
    return SuccessResponse(
        data=apartment_service.to_schema(
            data=apartment, schema_type=GetApartmentDetailsSchema
        )
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(IntegrityErrorException, auth=True, role=True),
    response_model=SuccessResponse[GetApartmentDetailsSchema],
)
@inject
async def create_apartment(
    request: Request,
    apartment_service: FromDishka[ApartmentService],
    data: CreateApartmentSchema = Body(),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetApartmentDetailsSchema]:
    apartment = await apartment_service.create_apartment(
        request=request, user_id=user.id, data=data
    )
    return SuccessResponse(
        data=apartment_service.to_schema(
            data=apartment, schema_type=GetApartmentDetailsSchema
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
