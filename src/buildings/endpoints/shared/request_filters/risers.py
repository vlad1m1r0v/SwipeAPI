from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.buildings.services import RiserService
from src.buildings.schemas.request import GetRiserSchema

from src.auth.dependencies import payload_from_token
from src.auth.enums import TokenType

from src.user.schemas import GetUserSchema

router = APIRouter(prefix="/risers")


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetRiserSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_risers_for_requests(
    riser_service: FromDishka[RiserService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    complex_id: int | None = Query(default=None),
    block_id: int | None = Query(default=None),
    section_id: int | None = Query(default=None),
    no: int | None = Query(default=None),
    _: GetUserSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[OffsetPagination[GetRiserSchema]]:
    results, total = await riser_service.get_risers_for_requests(
        limit=limit,
        offset=offset,
        complex_id=complex_id,
        block_id=block_id,
        section_id=section_id,
        no=no,
    )
    return SuccessResponse(
        data=riser_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetRiserSchema,
        )
    )
