from src.core.celery_app import celery  # noqa: F401

from src.auth.tasks import send_forgot_password_email  # noqa: F401
from src.users.tasks import monthly_withdrawal  # noqa: F401
