from dishka import AsyncContainer, Scope

from cli.utils import (
    create_notaries,
    create_users,
    create_builders,
    create_apartments,
    create_announcements,
    create_admin,
)


async def create_records(
    container: AsyncContainer,
):
    async with container(scope=Scope.REQUEST) as container:
        await create_notaries(container)
        users = await create_users(container)
        complexes, floors = await create_builders(container, users)
        apartments = await create_apartments(container, users, floors)
        announcements = await create_announcements(container, apartments, users)
        await create_admin(container, announcements)
