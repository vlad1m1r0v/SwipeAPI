from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.announcements.models import Complaint
from src.announcements.repositories import AnnouncementComplaintRepository


class AnnouncementComplaintService(
    SQLAlchemyAsyncRepositoryService[Complaint, AnnouncementComplaintRepository]
):
    repository_type = AnnouncementComplaintRepository

    async def get_admin_complaints(
        self, limit: int, offset: int, admin_id: int
    ) -> tuple[list[Complaint], int]:
        return await self.repository.get_admin_complaints(limit, offset, admin_id)

    async def get_complaint(self, complaint_id: int) -> Complaint:
        return await self.repository.get_complaint(complaint_id)
