from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.announcements.models import Announcement


class AnnouncementRepository(SQLAlchemyAsyncRepository[Announcement]):
    model_type = Announcement
