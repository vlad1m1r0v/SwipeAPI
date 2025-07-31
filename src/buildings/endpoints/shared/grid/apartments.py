from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.schemas import SuccessResponse
from src.core.utils import generate_examples

from src.auth.dependencies import payload_from_token
from src.auth.schemas import BasePayloadSchema
from src.auth.enums import TokenType

from src.apartments.services import ApartmentService
from src.apartments.schemas import GetApartmentGridListItem, GetApartmentGridDetail

router = APIRouter(prefix="/apartments")


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetApartmentGridListItem]],
    responses=generate_examples(auth=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_apartments(
    apartment_service: FromDishka[ApartmentService],
    section_id: int = Query(),
    price_min: int | None = Query(default=None),
    price_max: int | None = Query(default=None),
    price_min_per_m2: int | None = Query(default=None),
    price_max_per_m2: int | None = Query(default=None),
    area_min: int | None = Query(default=None),
    area_max: int | None = Query(default=None),
    finishing: str | None = Query(default=None),
    limit: int | None = Query(default=20),
    offset: int | None = Query(default=0),
    _: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[OffsetPagination[GetApartmentGridListItem]]:
    results, total = await apartment_service.get_apartments_list_for_grid(
        section_id=section_id,
        price_min=price_min,
        price_max=price_max,
        price_min_per_m2=price_min_per_m2,
        price_max_per_m2=price_max_per_m2,
        area_min=area_min,
        area_max=area_max,
        finishing=finishing,
        limit=limit,
        offset=offset,
    )
    return SuccessResponse(
        data=apartment_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetApartmentGridListItem,
        )
    )


@router.get(
    path="/{apartment_id}",
    response_model=SuccessResponse[GetApartmentGridDetail],
    responses=generate_examples(auth=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_apartment(
    apartment_service: FromDishka[ApartmentService],
    apartment_id: int,
    _: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[GetApartmentGridDetail]:
    result = await apartment_service.get_apartment_detail_for_grid(
        apartment_id=apartment_id
    )
    return SuccessResponse(
        data=apartment_service.to_schema(
            data=result, schema_type=GetApartmentGridDetail
        )
    )
