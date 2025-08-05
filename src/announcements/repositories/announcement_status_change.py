from datetime import datetime, UTC

from sqlalchemy import update
from sqlalchemy.orm import Session

from src.announcements.models import Announcement
from src.announcements.constants import RELEVANCE_PERIOD


class AnnouncementStatusChangeRepository:
    def __init__(self, session: Session):
        self._session = session

    def change_statuses(self):
        stmt = (
            update(Announcement)
            .where(Announcement.updated_at <= datetime.now(UTC) - RELEVANCE_PERIOD)
            .values(is_relevant=False)
        )

        self._session.execute(stmt)
