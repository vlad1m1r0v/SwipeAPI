from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.user.models import Subscription
from src.user.repositories import SubscriptionRepository


class SubscriptionService(
    SQLAlchemyAsyncRepositoryService[Subscription, SubscriptionRepository]
):
    repository_type = SubscriptionRepository
