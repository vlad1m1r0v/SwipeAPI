from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.builders.models import News
from src.builders.repositories import NewsRepository


class NewsService(SQLAlchemyAsyncRepositoryService[News, NewsRepository]):
    repository_type = NewsRepository
