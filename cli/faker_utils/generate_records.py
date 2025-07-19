from dishka import AsyncContainer, Scope

from cli.faker_utils.generate_users import generate_users
from src.user.services import UserService


async def generate_records(
    container: AsyncContainer,
):
    async with container(scope=Scope.REQUEST) as container:
        users_to_create = generate_users()

        user_service = await container.get(UserService)
        await user_service.create_many(users_to_create)
