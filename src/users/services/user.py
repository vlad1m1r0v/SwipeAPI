from typing import Sequence

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService, ModelDictT

from src.auth.utils import hash_password, validate_password

from src.users.models import User
from src.users.repositories import UserRepository
from src.users.enums import Role
from src.users.exceptions import UserDoesNotExistException, IncorrectPasswordException


class UserService(SQLAlchemyAsyncRepositoryService[User, UserRepository]):
    repository_type = UserRepository

    async def get_user_profile(self, item_id: int) -> User:
        return await self.repository.get_user_profile(item_id)

    async def get_builder_profile(self, item_id: int) -> User:
        return await self.repository.get_builder_profile(item_id)

    async def create_user(self, data: ModelDictT) -> User:
        data = data.model_dump()
        return await super().create(data={**data, "role": Role.USER})

    async def create_admin(self, data: ModelDictT) -> User:
        data = data.model_dump()
        return await super().create(data={**data, "role": Role.ADMIN})

    async def create_builder(self, data: ModelDictT) -> User:
        data = data.model_dump()
        return await super().create(data={**data, "role": Role.BUILDER})

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
        if isinstance(data, dict) and "password" in data:
            password: bytes | str | None = data.pop("password", None)
            if password is not None:
                hashed_password = hash_password(password)
                data.update({"password": hashed_password.decode()})
        return await super().to_model(data, operation)
