from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.builder.services import ComplexService

from src.auth.dependencies import payload_from_token
from src.auth.schemas import BasePayloadSchema
from src.auth.enums import TokenType

from src.buildings.schemas.request import GetComplexSchema

router = APIRouter(prefix="/complexes")


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetComplexSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_complexes_for_requests(
    complex_service: FromDishka[ComplexService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    search: str = Query(default=""),
    _: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[OffsetPagination[GetComplexSchema]]:
    results, total = await complex_service.get_complexes_for_requests(
        limit=limit, offset=offset, search=search
    )
    return SuccessResponse(
        data=complex_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetComplexSchema,
        )
    )
