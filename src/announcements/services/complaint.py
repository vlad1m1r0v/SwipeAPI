from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import Complaint
from src.announcements.repositories import AnnouncementComplaintRepository


class AnnouncementComplaintService(
    SQLAlchemyAsyncRepositoryService[Complaint, AnnouncementComplaintRepository]
):
    repository_type = AnnouncementComplaintRepository
