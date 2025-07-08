from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.exceptions import (
    IsNotOwnerException,
    IntegrityErrorException,
    NotFoundException,
    DuplicateKeyException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import builder_from_token

from src.builder.services import NewsService
from src.builder.dependencies import check_builder_owns_news
from src.builder.schemas import (
    GetBuilderSchema,
    GetNewsSchema,
    CreateNewsSchema,
    UpdateNewsSchema,
)

router = APIRouter(prefix="/news", tags=["Builder: News"])


@router.post(
    path="",
    response_model=SuccessResponse[GetNewsSchema],
    responses=generate_examples(IntegrityErrorException, auth=True, role=True),
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_news(
    news_service: FromDishka[NewsService],
    data: CreateNewsSchema,
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetNewsSchema]:
    news = await news_service.create(
        {"complex_id": builder.complex.id, **data.model_dump()}
    )
    return SuccessResponse(
        data=news_service.to_schema(data=news, schema_type=GetNewsSchema)
    )


@router.patch(
    path="/{news_id}",
    response_model=SuccessResponse[GetNewsSchema],
    responses=generate_examples(
        DuplicateKeyException,
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
)
@inject
async def update_news(
    news_id: int,
    news_service: FromDishka[NewsService],
    data: UpdateNewsSchema,
    _: GetBuilderSchema = Depends(check_builder_owns_news),
) -> SuccessResponse[GetNewsSchema]:
    news = await news_service.update(
        data=data.model_dump(exclude_none=True), item_id=news_id
    )
    return SuccessResponse(
        data=news_service.to_schema(data=news, schema_type=GetNewsSchema)
    )


@router.delete(
    path="/{news_id}",
    response_model=SuccessResponse,
    responses=generate_examples(
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_news(
    news_id: int,
    news_service: FromDishka[NewsService],
    _: GetBuilderSchema = Depends(check_builder_owns_news),
):
    await news_service.delete(item_id=news_id)
    return SuccessResponse(message="News has been deleted successfully.")
