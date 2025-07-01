from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.builder.models import News


class NewsRepository(SQLAlchemyAsyncRepository[News]):
    model_type = News
