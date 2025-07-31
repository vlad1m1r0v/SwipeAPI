from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination

from src.core.schemas import SuccessResponse
from src.core.utils import generate_examples

from src.auth.dependencies import payload_from_token
from src.auth.schemas import BasePayloadSchema
from src.auth.enums import TokenType

from src.buildings.schemas.grid import GetSectionSchema
from src.buildings.services import SectionService

router = APIRouter(prefix="/sections")


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetSectionSchema]],
    responses=generate_examples(auth=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_sections(
    section_service: FromDishka[SectionService],
    block_id: int = Query(),
    _: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[OffsetPagination[GetSectionSchema]]:
    results = await section_service.get_sections_for_grid(block_id)
    return SuccessResponse(
        data=section_service.to_schema(data=results, schema_type=GetSectionSchema)
    )
