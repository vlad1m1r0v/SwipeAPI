from typing import Sequence

from advanced_alchemy.filters import LimitOffset, SearchFilter
from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from sqlalchemy import orm, select, insert

from src.auth.utils import hash_password
from src.auth.schemas import RegisterSchema

from src.user.enums import Role
from src.user.models import (
    User,
    Contact,
    AgentContact,
    Subscription,
    NotificationSettings,
    Balance,
)

from src.admin.models import Blacklist

from src.builder.models import (
    Complex,
    Infrastructure,
    Advantages,
    FormalizationAndPaymentSettings,
)


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User

    async def create_user(self, data: RegisterSchema) -> User:
        fields = data.model_dump()
        password = fields.pop("password")

        stmt = (
            insert(User)
            .values(**fields, role=Role.USER, password=str(hash_password(password)))
            .returning(User)
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        inserts = [
            insert(Contact).values(user_id=user.id, email=user.email, phone=user.phone),
            insert(AgentContact).values(user_id=user.id),
            insert(Subscription).values(user_id=user.id),
            insert(NotificationSettings).values(user_id=user.id),
            insert(Balance).values(user_id=user.id),
        ]
        for stmt in inserts:
            await self.session.execute(stmt)

        return user

    async def create_admin(self, data: RegisterSchema) -> User:
        fields = data.model_dump()
        password = fields.pop("password")

        stmt = (
            insert(User)
            .values(**fields, role=Role.ADMIN, password=str(hash_password(password)))
            .returning(User)
        )
        result = await self.session.execute(stmt)
        admin = result.scalar_one_or_none()
        return admin

    async def create_builder(self, data: RegisterSchema) -> User:
        fields = data.model_dump()
        password = fields.pop("password")

        stmt = (
            insert(User)
            .values(**fields, role=Role.USER, password=str(hash_password(password)))
            .returning(User)
        )
        result = await self.session.execute(stmt)
        builder = result.scalar_one_or_none()

        await self.session.execute(
            insert(Contact).values(
                user_id=builder.id, email=builder.email, phone=builder.phone
            )
        )

        result = await self.session.execute(
            insert(Complex).values(user_id=builder.id, name=builder.name)
        )
        building = result.scalar_one_or_none()

        inserts = [
            insert(Infrastructure).values(user_id=building.id),
            insert(Advantages).values(user_id=building.id),
            insert(FormalizationAndPaymentSettings).values(user_id=building.id),
        ]
        for stmt in inserts:
            await self.session.execute(stmt)

        return builder

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
