from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import payload_from_token
from src.auth.enums import TokenType
from src.auth.schemas import BasePayloadSchema

from src.buildings.schemas.request import GetBlockSchema
from src.buildings.services import BlockService

router = APIRouter(prefix="/blocks")


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetBlockSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_blocks_for_requests(
    block_service: FromDishka[BlockService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    complex_id: int | None = Query(default=None),
    no: int | None = Query(default=None),
    _: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[OffsetPagination[GetBlockSchema]]:
    results, total = await block_service.get_blocks_for_requests(
        limit=limit, offset=offset, complex_id=complex_id, no=no
    )
    return SuccessResponse(
        data=block_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetBlockSchema,
        )
    )
