from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.users.models import Subscription
from src.users.repositories import SubscriptionRepository


class SubscriptionService(
    SQLAlchemyAsyncRepositoryService[Subscription, SubscriptionRepository]
):
    repository_type = SubscriptionRepository