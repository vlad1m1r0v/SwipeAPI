from src.core.celery_app import celery

from src.auth.tasks import send_forgot_password_email
