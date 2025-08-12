from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from src.user.constants import WITHDRAWAL, MONTH_DELTA
from src.user.exceptions import NotEnoughMoneyException
from src.user.models import Subscription, User, Balance


class SubscriptionRepository(SQLAlchemyAsyncRepository[Subscription]):
    model_type = Subscription

    async def renew_user_subscription(self, item_id: int) -> Subscription:
        stmt = (
            select(User)
            .join(Subscription, Subscription.user_id == User.id)
            .join(Balance, Balance.user_id == User.id)
            .options(joinedload(User.balance))
            .where(User.id == item_id)
        )

        result = await self.session.execute(stmt)
        user: User = result.scalar_one_or_none()

        if user.balance.value < WITHDRAWAL:
            raise NotEnoughMoneyException()

        stmt = (
            update(Balance)
            .where(Balance.user_id == item_id)
            .values(value=Balance.value - WITHDRAWAL)
        )
        await self.session.execute(stmt)

        stmt = (
            update(Subscription)
            .where(Subscription.user_id == item_id)
            .values(expiry_date=Subscription.expiry_date + MONTH_DELTA)
            .returning(Subscription)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
