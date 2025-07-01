from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builder.models import News
from src.builder.repositories import NewsRepository


class NewsService(SQLAlchemyAsyncRepositoryService[News, NewsRepository]):
    repository_type = NewsRepository
