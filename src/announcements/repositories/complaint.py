from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.announcements.models import Complaint


class AnnouncementComplaintRepository(SQLAlchemyAsyncRepository[Complaint]):
    model_type = Complaint
