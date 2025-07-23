from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import Announcement
from src.announcements.repositories import AnnouncementRepository


class AnnouncementService(
    SQLAlchemyAsyncRepositoryService[Announcement, AnnouncementRepository]
):
    repository_type = AnnouncementRepository
