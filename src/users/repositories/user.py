from typing import Sequence

from advanced_alchemy.filters import LimitOffset, SearchFilter
from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from sqlalchemy import orm, select

from src.users.models import User

from src.admins.models import Blacklist

from src.builders.models import Complex


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User

    async def get_user_profile(self, item_id: int) -> User:
        return await self.get(
            item_id=item_id,
            load=[
                orm.joinedload(User.contact),
                orm.joinedload(User.agent_contact),
                orm.joinedload(User.subscription),
                orm.joinedload(User.notification_settings),
                orm.joinedload(User.balance),
            ],
        )

    async def get_builder_profile(self, item_id) -> User:
        return await self.get(
            item_id=item_id,
            load=[
                orm.selectinload(User.contact),
                orm.selectinload(User.complex),
                orm.selectinload(User.complex).selectinload(Complex.infrastructure),
                orm.selectinload(User.complex).selectinload(Complex.advantages),
                orm.selectinload(User.complex).selectinload(
                    Complex.formalization_and_payment_settings
                ),
                orm.selectinload(User.complex).selectinload(Complex.news),
                orm.selectinload(User.complex).selectinload(Complex.documents),
            ],
        )

    async def get_blacklisted_users(
        self, limit: int, offset: int, search: str
    ) -> tuple[Sequence[User], int]:
        limit_offset = LimitOffset(limit=limit, offset=offset)
        search_filter = SearchFilter(
            field_name={"name", "email", "phone"},
            value=search,
            ignore_case=True,
        )

        stmt = select(User).join(Blacklist, User.id == Blacklist.user_id)

        results, total = await self.list_and_count(
            limit_offset,
            search_filter,
            statement=stmt.options(orm.joinedload(User.blacklist)),
        )

        return results, total
