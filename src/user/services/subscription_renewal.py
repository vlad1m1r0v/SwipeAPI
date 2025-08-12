from sqlalchemy.orm import Session

from src.user.repositories import SubscriptionRenewalRepository


class SubscriptionRenewalService:
    def __init__(self, session: Session):
        self.repo = SubscriptionRenewalRepository(session=session)

    def renew_subscriptions(self):
        return self.repo.renew_subscriptions()
