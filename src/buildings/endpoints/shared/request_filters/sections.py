from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.buildings.services import SectionService
from src.buildings.schemas.request import GetSectionSchema

from src.auth.dependencies import payload_from_token
from src.auth.enums import TokenType

from src.user.schemas import GetUserSchema

router = APIRouter(prefix="/sections")


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetSectionSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_sections_for_requests(
    section_service: FromDishka[SectionService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    complex_id: int | None = Query(default=None),
    block_id: int | None = Query(default=None),
    no: int | None = Query(default=None),
    _: GetUserSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[OffsetPagination[GetSectionSchema]]:
    results, total = await section_service.get_sections_for_requests(
        limit=limit,
        offset=offset,
        complex_id=complex_id,
        block_id=block_id,
        no=no,
    )
    return SuccessResponse(
        data=section_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetSectionSchema,
        )
    )
