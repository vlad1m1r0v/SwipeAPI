from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, status, Query, Depends, Body

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.exceptions import (
    IntegrityErrorException,
    IsNotOwnerException,
    NotFoundException,
)
from src.core.schemas import SuccessResponse
from src.core.utils import generate_examples

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

from src.builder.schemas import (
    GetFavouriteComplexListItemSchema,
    GetFavouriteComplexDetailSchema,
    CreateFavouriteComplexSchema,
)
from src.builder.services import FavouriteComplexService
from src.builder.dependencies import check_user_owns_favourite_complex

router = APIRouter(
    prefix="/user/favourite-complexes", tags=["User: Favourite Complexes"]
)


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetFavouriteComplexListItemSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_favourite_complexes(
    favourite_complex_service: FromDishka[FavouriteComplexService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetFavouriteComplexListItemSchema]]:
    results, total = await favourite_complex_service.get_favourite_complexes(
        limit=limit, offset=offset, user_id=user.id
    )
    return SuccessResponse(
        data=favourite_complex_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetFavouriteComplexListItemSchema,
        )
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        IntegrityErrorException, auth=True, role=True, user=True
    ),
    response_model=SuccessResponse[GetFavouriteComplexDetailSchema],
)
@inject
async def create_favourite_complex(
    favourite_complex_service: FromDishka[FavouriteComplexService],
    data: CreateFavouriteComplexSchema = Body(),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetFavouriteComplexDetailSchema]:
    created = await favourite_complex_service.create(
        data={"user_id": user.id, **data.model_dump()}
    )
    return SuccessResponse(
        data=favourite_complex_service.to_schema(
            data=await favourite_complex_service.get_favourite_complex_detail(
                created.id
            ),
            schema_type=GetFavouriteComplexDetailSchema,
        )
    )


@router.delete(
    path="/{favourite_id}",
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
async def delete_favourite_complex(
    favourite_complex_service: FromDishka[FavouriteComplexService],
    favourite_id: int,
    _: GetUserSchema = Depends(check_user_owns_favourite_complex),
):
    await favourite_complex_service.delete(item_id=favourite_id)
    return SuccessResponse(
        message="Complex has been removed from favourites successfully."
    )
