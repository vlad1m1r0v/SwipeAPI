from datetime import datetime, timedelta

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService, ModelDictT

from src.users.models import (
    UserModel,
    ContactModel,
    AgentContactModel,
    BalanceModel,
    SubscriptionModel,
    NotificationSettingsModel
)
from src.users.repositories import UserRepository


class UserService(SQLAlchemyAsyncRepositoryService[UserModel, UserRepository]):
    repository_type = UserRepository

    async def create(self, data: ModelDictT, **kwargs) -> UserModel:
        async with self.repository.session.begin():
            user = UserModel(**data.model_dump())
            self.repository.session.add(user)
            await self.repository.session.flush()

            self.repository.session.add_all([
                ContactModel(
                    user_id=user.id,
                    email=user.email,
                    phone=user.phone,
                ),
                AgentContactModel(
                    user_id=user.id,
                ),
                BalanceModel(
                    user_id=user.id,
                ),
                SubscriptionModel(
                    user_id=user.id,
                    expiry_date=datetime.utcnow() + timedelta(days=30),
                ),
                NotificationSettingsModel(
                    user_id=user.id,
                ),
            ])

        return user
