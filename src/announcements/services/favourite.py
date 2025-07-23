from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import FavouriteAnnouncement
from src.announcements.repositories import AnnouncementFavouriteRepository


class AnnouncementFavouriteService(
    SQLAlchemyAsyncRepositoryService[
        FavouriteAnnouncement, AnnouncementFavouriteRepository
    ]
):
    repository_type = AnnouncementFavouriteRepository
