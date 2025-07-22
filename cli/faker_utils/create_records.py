from dishka import AsyncContainer, Scope

from cli.faker_utils.create_users import create_users
from cli.faker_utils.create_builders import create_builders


async def create_records(
    container: AsyncContainer,
):
    async with container(scope=Scope.REQUEST) as container:
        await create_users(container)
        await create_builders(container)
