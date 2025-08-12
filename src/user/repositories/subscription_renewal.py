from datetime import datetime, UTC

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.user.constants import WITHDRAWAL, MONTH_DELTA
from src.user.models import Subscription, User, Balance


class SubscriptionRenewalRepository:
    def __init__(self, session: Session):
        self._session = session

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
        result = self._session.execute(stmt)

        user_ids = [row[0] for row in result.all()]

        stmt_withdraw = (
            update(Balance)
            .where(Balance.user_id.in_(user_ids))
            .values(value=Balance.value - WITHDRAWAL)
        )
        self._session.execute(stmt_withdraw)

        new_expiry = now + MONTH_DELTA

        stmt_renew = (
            update(Subscription)
            .where(Subscription.user_id.in_(user_ids))
            .values(expiry_date=new_expiry)
        )
        self._session.execute(stmt_renew)
