from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import Filter
from src.announcements.repositories import AnnouncementFilterRepository


class AnnouncementFilterService(
    SQLAlchemyAsyncRepositoryService[Filter, AnnouncementFilterRepository]
):
    repository_type = AnnouncementFilterRepository
