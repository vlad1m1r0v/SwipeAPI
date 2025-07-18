import logging
from dishka import AsyncContainer, Scope

from cli.faker_utils.generate_users import generate_users
from src.user.services import UserService

logger = logging.getLogger(__name__)  # створюємо логер з ім'ям модуля


async def generate_records(
    container: AsyncContainer,
):
    logger.info("Starting to generate user records...")

    async with container(scope=Scope.REQUEST) as container:
        users_to_create = generate_users()
        logger.info(f"Generated {len(users_to_create)} users.")

        user_service = await container.get(UserService)
        await user_service.create_many(users_to_create)

        logger.info("Finished creating users.")
