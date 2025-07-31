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

from src.notaries.services import NotaryService
from src.notaries.schemas import GetNotarySchema

router = APIRouter(prefix="/notaries", tags=["Shared: Notaries"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetNotarySchema]],
    responses=generate_examples(auth=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_notaries(
    notary_service: FromDishka[NotaryService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    search: str = Query(default=""),
    _: BasePayloadSchema = Depends(payload_from_token(TokenType.ACCESS_TOKEN)),
) -> SuccessResponse[OffsetPagination[GetNotarySchema]]:
    results, total = await notary_service.get_notaries(limit, offset, search)
    return SuccessResponse(
        data=notary_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetNotarySchema,
        )
    )
