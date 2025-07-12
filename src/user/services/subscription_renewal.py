from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.user.models import Subscription
from src.user.repositories import SubscriptionRenewalRepository


class SubscriptionRenewalService:
    def __init__(self, session: Session, async_session: AsyncSession):
        self.repo = SubscriptionRenewalRepository(
            session=session,
            async_session=async_session,
        )

    def renew_subscriptions(self):
        return self.repo.renew_subscriptions()

    async def renew_user_subscription(self, item_id: int) -> Subscription:
        return await self.repo.renew_user_subscription(item_id)
