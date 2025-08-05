from sqlalchemy.orm import Session

from src.announcements.repositories import AnnouncementStatusChangeRepository


class AnnouncementStatusChangeService:
    def __init__(self, session: Session):
        self.repo = AnnouncementStatusChangeRepository(session=session)

    def change_statuses(self):
        return self.repo.change_statuses()
