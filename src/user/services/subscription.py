from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.user.models import Subscription
from src.user.repositories import SubscriptionRepository


class SubscriptionService(
    SQLAlchemyAsyncRepositoryService[Subscription, SubscriptionRepository]
):
    repository_type = SubscriptionRepository

    async def renew_user_subscription(self, item_id: int) -> Subscription:
        return await self.repository.renew_user_subscription(item_id)
