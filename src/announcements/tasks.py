from dishka.integrations.celery import inject
from dishka import FromDishka

from src.core.celery_app import celery

from src.announcements.services import AnnouncementStatusChangeService


@celery.task(name="daily_announcement_status_change")
@inject
def daily_announcement_status_change(
    announcement_status_change_service: FromDishka[AnnouncementStatusChangeService],
):
    announcement_status_change_service.change_statuses()
