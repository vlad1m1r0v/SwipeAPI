from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.builder.schemas import GetComplexIdAndNoSchema
from src.builder.services import ComplexService

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

complexes = APIRouter(
    prefix="/add-to-complex-request/complexes", tags=["User: Add to complex requests"]
)


@complexes.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetComplexIdAndNoSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_complexes_for_filters(
    complex_service: FromDishka[ComplexService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    search: str = Query(default=""),
    _: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetComplexIdAndNoSchema]]:
    results, total = await complex_service.get_complexes_for_filters(
        limit=limit, offset=offset, search=search
    )
    return SuccessResponse(
        data=complex_service.to_schema(
            data=results, total=total, schema_type=GetComplexIdAndNoSchema
        )
    )
