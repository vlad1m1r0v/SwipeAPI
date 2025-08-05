from src.core.celery_app import celery  # noqa: F401

from src.auth.tasks import send_forgot_password_email  # noqa: F401
from src.user.tasks import daily_withdrawal  # noqa: F401
from src.announcements.tasks import daily_announcement_status_change  # noqa: F401
