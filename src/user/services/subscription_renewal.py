from datetime import datetime, UTC

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from src.user.constants import WITHDRAWAL, MONTH_DELTA
from src.user.exceptions import NotEnoughMoneyException
from src.user.models import Subscription, User, Balance


class SubscriptionRenewalService:
    def __init__(self, session: Session, async_session: AsyncSession):
        self._sync_session = session
        self._async_session = async_session

    def renew_subscriptions(self):
        now = datetime.now(UTC)

        stmt = (
            select(User.id)
            .join(Subscription, Subscription.user_id == User.id)
            .join(Balance, Balance.user_id == User.id)
            .where(
                Subscription.expiry_date <= now,
                Subscription.is_auto_renewal.is_(True),
                Balance.value >= WITHDRAWAL,
            )
        )
        result = self._sync_session.execute(stmt)

        user_ids = [row[0] for row in result.all()]

        stmt_withdraw = (
            update(Balance)
            .where(Balance.user_id.in_(user_ids))
            .values(value=Balance.value - WITHDRAWAL)
        )
        self._sync_session.execute(stmt_withdraw)

        new_expiry = now + MONTH_DELTA

        stmt_renew = (
            update(Subscription)
            .where(Subscription.user_id.in_(user_ids))
            .values(expiry_date=new_expiry)
        )
        self._sync_session.execute(stmt_renew)

    async def renew_user_subscription(self, item_id: int):
        stmt = (
            select(User)
            .join(Subscription, Subscription.user_id == User.id)
            .join(Balance, Balance.user_id == User.id)
            .options(joinedload(User.balance))
            .where(User.id == item_id)
        )

        result = await self._async_session.execute(stmt)
        user: User = result.scalar_one_or_none()

        if user.balance.value < WITHDRAWAL:
            raise NotEnoughMoneyException()

        stmt = (
            update(Balance)
            .where(Balance.user_id == item_id)
            .values(value=Balance.value - WITHDRAWAL)
        )
        await self._async_session.execute(stmt)

        stmt = (
            update(Subscription)
            .where(Subscription.user_id == item_id)
            .values(expiry_date=Subscription.expiry_date + MONTH_DELTA)
        )

        await self._async_session.execute(stmt)
