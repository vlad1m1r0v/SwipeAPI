from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.builders.services import NewsService

from src.auth.dependencies import builder_from_token

from src.builders.schemas import GetBuilderSchema
from src.core.exceptions import IsNotOwnerException


@inject
async def check_builder_owns_news(
    news_id: int,
    news_service: FromDishka[NewsService],
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    news = await news_service.get(item_id=news_id)

    if news.complex_id != builder.complex.id:
        raise IsNotOwnerException()

    return builder
