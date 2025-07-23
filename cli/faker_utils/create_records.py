from dishka import AsyncContainer, Scope

from cli.faker_utils.create_users import create_users
from cli.faker_utils.create_builders import create_builders
from cli.faker_utils.create_apartments import create_apartments


async def create_records(
    container: AsyncContainer,
):
    async with container(scope=Scope.REQUEST) as container:
        users = await create_users(container)
        complexes, floors = await create_builders(container)
        await create_apartments(container, users, floors)
