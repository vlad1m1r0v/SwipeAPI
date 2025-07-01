from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.user.models import Subscription


class SubscriptionRepository(SQLAlchemyAsyncRepository[Subscription]):
    model_type = Subscription
