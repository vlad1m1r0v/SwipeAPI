from typing import Sequence

from advanced_alchemy.filters import LimitOffset, SearchFilter, ComparisonFilter
from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from sqlalchemy import orm, select, func, insert

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

from src.apartments.models import Apartment

from src.buildings.models import Riser, Section, Block, Floor


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User

    async def create_user(self, data: RegisterSchema) -> User:
        fields = data.model_dump()
        password = fields.pop("password")

        stmt = (
            insert(User)
            .values(**fields, role=Role.USER, password=hash_password(password).decode())
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
            .values(
                **fields, role=Role.ADMIN, password=hash_password(password).decode()
            )
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
            .values(
                **fields, role=Role.BUILDER, password=hash_password(password).decode()
            )
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
            insert(Complex)
            .values(user_id=builder.id, name=builder.name)
            .returning(Complex)
        )
        building: Complex = result.scalar_one_or_none()

        inserts = [
            insert(Infrastructure).values(complex_id=building.id),
            insert(Advantages).values(complex_id=building.id),
            insert(FormalizationAndPaymentSettings).values(complex_id=building.id),
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
        builder: User = result.scalar_one_or_none()

        agg_stmt = (
            select(
                func.min(Apartment.price).label("min_price"),
                (func.sum(Apartment.price) / func.sum(Apartment.area)).label(
                    "avg_price_per_m2"
                ),
                func.min(Apartment.area).label("min_area"),
                func.max(Apartment.area).label("max_area"),
            )
            .join(Riser, Riser.id == Apartment.riser_id)
            .join(Section, Section.id == Riser.section_id)
            .join(Block, Block.id == Section.block_id)
            .join(Floor, Floor.id == Apartment.floor_id)
            .where(Block.complex_id == builder.complex.id, Floor.block_id == Block.id)
        )

        result = await self.session.execute(agg_stmt)
        agg = result.first()

        builder.complex.min_price = agg.min_price
        builder.complex.avg_price_per_m2 = agg.avg_price_per_m2
        builder.complex.min_area = agg.min_area
        builder.complex.max_area = agg.max_area

        stmt = (
            select(
                Block.id, Block.no, func.count(Apartment.id).label("apartments_count")
            )
            .join(Section, Section.block_id == Block.id)
            .join(Riser, Riser.section_id == Section.id)
            .join(Apartment, Apartment.riser_id == Riser.id)
            .where(Block.complex_id == builder.complex.id)
            .group_by(Block.id)
            .order_by(Block.no)
        )

        result = await self.session.execute(stmt)
        builder.complex.apartments_per_block = result.all()

        return builder

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

    async def get_users(
        self, limit: int, offset: int, search: str
    ) -> tuple[Sequence[User], int]:
        limit_offset = LimitOffset(limit=limit, offset=offset)
        search_filter = SearchFilter(
            field_name={"name", "email", "phone"},
            value=search,
            ignore_case=True,
        )

        role_filter = ComparisonFilter(
            field_name="role",
            operator="eq",
            value=Role.USER,
        )

        results, total = await self.list_and_count(
            limit_offset, search_filter, role_filter
        )
        return results, total
