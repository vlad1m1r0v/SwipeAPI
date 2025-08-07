from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from src.core.schemas import SuccessResponse
from src.core.utils import generate_examples

from src.auth.dependencies import payload_from_token
from src.auth.schemas import BasePayloadSchema
from src.auth.enums import TokenType

from src.buildings.schemas.grid import GetFloorGridSchema
from src.buildings.services import GridService

router = APIRouter(prefix="/layout")


@router.get(
    path="",
    response_model=SuccessResponse[list[GetFloorGridSchema]],
    responses=generate_examples(auth=True, user=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_layout(
    grid_service: FromDishka[GridService],
    section_id: int = Query(),
    _: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[list[GetFloorGridSchema]]:
    results = await grid_service.get_layout(section_id)
    return SuccessResponse(data=results)
