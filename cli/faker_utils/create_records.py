from dishka import AsyncContainer, Scope

from cli.faker_utils.create_users import create_users


async def create_records(
    container: AsyncContainer,
):
    async with container(scope=Scope.REQUEST) as container:
        await create_users(container)
