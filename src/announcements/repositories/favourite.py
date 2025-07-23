from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.announcements.models import FavouriteAnnouncement


class AnnouncementFavouriteRepository(SQLAlchemyAsyncRepository[FavouriteAnnouncement]):
    model_type = FavouriteAnnouncement
