from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.users.models import Subscription


class SubscriptionRepository(SQLAlchemyAsyncRepository[Subscription]):
    model_type = Subscription