from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends

from src.user.services import UserService

from src.auth.dependencies import builder_from_token

from src.builder.services import NewsService
from src.builder.dependencies import check_builder_owns_news
from src.builder.schemas import GetBuilderSchema, CreateNewsSchema, UpdateNewsSchema

router = APIRouter(prefix="/news", tags=["Builder: News"])


@router.post("", response_model=GetBuilderSchema)
@inject
async def create_news(
    news_service: FromDishka[NewsService],
    user_service: FromDishka[UserService],
    data: CreateNewsSchema,
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    await news_service.create({"complex_id": builder.complex.id, **data.model_dump()})
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)


@router.patch("/{news_id}", response_model=GetBuilderSchema)
@inject
async def update_news(
    news_id: int,
    news_service: FromDishka[NewsService],
    user_service: FromDishka[UserService],
    data: UpdateNewsSchema,
    builder: GetBuilderSchema = Depends(check_builder_owns_news),
) -> GetBuilderSchema:
    await news_service.update(data=data.model_dump(exclude_none=True), item_id=news_id)
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)


@router.delete("/{news_id}", response_model=GetBuilderSchema)
@inject
async def delete_news(
    news_id: int,
    news_service: FromDishka[NewsService],
    user_service: FromDishka[UserService],
    builder: GetBuilderSchema = Depends(check_builder_owns_news),
):
    await news_service.delete(item_id=news_id)
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)
