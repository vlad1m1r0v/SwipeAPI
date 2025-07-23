from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import AnnouncementView
from src.announcements.repositories import AnnouncementViewRepository


class AnnouncementViewService(
    SQLAlchemyAsyncRepositoryService[AnnouncementView, AnnouncementViewRepository]
):
    repository_type = AnnouncementViewRepository
