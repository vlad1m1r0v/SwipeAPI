from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.users.models import UserModel
from src.users.repositories import UserRepository


class UserService(SQLAlchemyAsyncRepositoryService[UserModel, UserRepository]):
    repository_type = UserRepository
