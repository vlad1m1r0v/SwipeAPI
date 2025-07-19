from typing import Sequence

from pydantic import BaseModel

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService, ModelDictT

from src.auth.utils import hash_password, validate_password

from src.user.models import User
from src.user.repositories import UserRepository
from src.user.exceptions import UserDoesNotExistException, IncorrectPasswordException


class UserService(SQLAlchemyAsyncRepositoryService[User, UserRepository]):
    repository_type = UserRepository

    async def get_user_profile(self, item_id: int) -> User:
        return await self.repository.get_user_profile(item_id)

    async def get_builder_profile(self, item_id: int) -> User:
        return await self.repository.get_builder_profile(item_id)

    async def create_user(self, data: ModelDictT) -> User:
        return await self.repository.create_user(data)

    async def create_admin(self, data: ModelDictT) -> User:
        return await self.repository.create_admin(data)

    async def create_builder(self, data: ModelDictT) -> User:
        return await self.repository.create_builder(data)

    async def get_blacklisted_users(
        self, limit: int, offset: int, search: str
    ) -> tuple[Sequence[User], int]:
        return await self.repository.get_blacklisted_users(
            limit=limit, offset=offset, search=search
        )

    async def authenticate(self, data: ModelDictT) -> User:
        user = await self.get_one_or_none(email=data.email)

        if not user:
            raise UserDoesNotExistException()

        if not validate_password(data.password, user.password.encode()):
            raise IncorrectPasswordException()

        return user

    async def update_password(self, item_id: int, data: ModelDictT) -> None:
        user = await self.get_one_or_none(id=item_id)

        if not user:
            raise UserDoesNotExistException()

        if not validate_password(data["old_password"], user.password.encode()):
            raise IncorrectPasswordException()

        await self.update(data={"password": data["new_password"]}, item_id=user.id)

    async def to_model(self, data: ModelDictT, operation: str | None = None) -> User:
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_unset=True)

        if "password" in data:
            password: bytes | str | None = data.pop("password", None)

            if password is not None:
                hashed_password = hash_password(password)
                data.update({"password": hashed_password.decode()})

        return await super().to_model(data, operation)
