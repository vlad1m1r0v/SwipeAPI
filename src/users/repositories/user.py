from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.users.models import UserModel


class UserRepository(SQLAlchemyAsyncRepository[UserModel]):

    model_type = UserModel