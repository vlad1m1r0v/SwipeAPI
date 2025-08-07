from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.exceptions import NotFoundException
from src.core.schemas import SuccessResponse
from src.core.utils import generate_examples

from src.auth.dependencies import payload_from_token
from src.auth.schemas import BasePayloadSchema
from src.auth.enums import TokenType

from src.builder.services import ComplexService
from src.builder.schemas import GetComplexFeedListItemSchema, GetComplexFeedDetailSchema

router = APIRouter(prefix="/complexes", tags=["Shared: Complexes"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetComplexFeedListItemSchema]],
    responses=generate_examples(auth=True, user=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_complexes_for_feed_list(
    complex_service: FromDishka[ComplexService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    _: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[OffsetPagination[GetComplexFeedListItemSchema]]:
    results, total = await complex_service.get_complexes_for_feed_list(limit, offset)
    return SuccessResponse(
        data=complex_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetComplexFeedListItemSchema,
        )
    )


@router.get(
    path="/{complex_id}",
    response_model=SuccessResponse[GetComplexFeedDetailSchema],
    responses=generate_examples(NotFoundException, auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_complex_detail(
    complex_service: FromDishka[ComplexService],
    complex_id: int,
    _: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[GetComplexFeedDetailSchema]:
    building = await complex_service.get_complex_detail(complex_id)
    return SuccessResponse(
        data=complex_service.to_schema(
            data=building, schema_type=GetComplexFeedDetailSchema
        )
    )
