import os

from sqlalchemy import true

from dishka import AsyncContainer, Scope

from src.core.constants import MEDIA_DIR

from src.user.services import UserService

from src.notaries.services import NotaryService


async def clear_records(container: AsyncContainer) -> None:
    for filename in os.listdir(MEDIA_DIR):
        file_path = os.path.join(MEDIA_DIR, filename)
        os.remove(file_path)

    async with container(scope=Scope.REQUEST) as container:
        user_service = await container.get(UserService)
        await user_service.delete_where(true())

        notary_service = await container.get(NotaryService)
        await notary_service.delete_where(true())
