from dishka.integrations.celery import inject
from dishka import FromDishka

from src.core.celery_app import celery

from src.users.services import SubscriptionRenewalService


@celery.task(name="daily_withdrawal")
@inject
def daily_withdrawal(
    subscription_renewal_service: FromDishka[SubscriptionRenewalService],
):
    subscription_renewal_service.renew_subscriptions()
