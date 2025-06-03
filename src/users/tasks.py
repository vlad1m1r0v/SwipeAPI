import logging

from dishka.integrations.celery import inject
from dishka import FromDishka

from src.core.celery_app import celery

from src.users.services import MonthlyWithdrawalService

logger = logging.getLogger(__name__)


@celery.task(name="monthly_withdrawal")
@inject
def monthly_withdrawal(
    monthly_withdrawal_service: FromDishka[MonthlyWithdrawalService],
):
    monthly_withdrawal_service.renew_subscriptions()
