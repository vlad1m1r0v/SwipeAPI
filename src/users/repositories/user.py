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
        stmt = (
            select(User)
            .where(User.id == item_id)
            .options(
                orm.joinedload(User.contact),
                orm.joinedload(User.complex),
                orm.joinedload(User.complex).joinedload(Complex.infrastructure),
                orm.joinedload(User.complex).joinedload(Complex.advantages),
                orm.joinedload(User.complex).joinedload(
                    Complex.formalization_and_payment_settings
                ),
                orm.joinedload(User.complex).selectinload(Complex.news),
                orm.joinedload(User.complex).selectinload(Complex.documents),
                orm.joinedload(User.complex).selectinload(Complex.gallery),
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

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
