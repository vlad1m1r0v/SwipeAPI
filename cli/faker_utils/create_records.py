from dishka import AsyncContainer, Scope

from cli.faker_utils.create_notaries import create_notaries
from cli.faker_utils.create_users import create_users
from cli.faker_utils.create_builders import create_builders
from cli.faker_utils.create_apartments import create_apartments
from cli.faker_utils.create_announcements import create_announcements


async def create_records(
    container: AsyncContainer,
):
    async with container(scope=Scope.REQUEST) as container:
        await create_notaries(container)
        users = await create_users(container)
        complexes, floors = await create_builders(container)
        apartments = await create_apartments(container, users, floors)
        await create_announcements(container, apartments, users)
