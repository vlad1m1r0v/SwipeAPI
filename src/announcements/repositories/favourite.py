from typing import Sequence, Any

from sqlalchemy.orm import joinedload
from sqlalchemy import select, func, Select

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset

from src.announcements.models import (
    Announcement,
    FavouriteAnnouncement,
)

from src.apartments.models import Apartment

from src.user.models import User

from src.buildings.models import Block, Floor, Section, Riser


class AnnouncementFavouriteRepository(SQLAlchemyAsyncRepository[FavouriteAnnouncement]):
    model_type = FavouriteAnnouncement

    async def get_favourite_user_announcements(
        self, user_id: int, limit: int, offset: int
    ) -> tuple[Sequence[FavouriteAnnouncement], int]:
        total_floors_subquery = (
            select(
                Floor.block_id.label("block_id"),
                func.count(Floor.id).label("total_floors"),
            )
            .group_by(Floor.block_id)
            .subquery()
        )

        stmt = (
            select(
                FavouriteAnnouncement,
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
            )
            .join(
                Announcement, FavouriteAnnouncement.announcement_id == Announcement.id
            )
            .join(Apartment, Announcement.apartment_id == Apartment.id)
            .outerjoin(Floor, Apartment.floor_id == Floor.id)
            .outerjoin(Riser, Apartment.riser_id == Riser.id)
            .outerjoin(Section, Riser.section_id == Section.id)
            .outerjoin(Block, Section.block_id == Block.id)
            .outerjoin(
                total_floors_subquery, Block.id == total_floors_subquery.c.block_id
            )
            .where(FavouriteAnnouncement.user_id == user_id)
            .options(
                joinedload(FavouriteAnnouncement.announcement)
                .joinedload(Announcement.apartment)
                .selectinload(Apartment.gallery),
                joinedload(FavouriteAnnouncement.announcement).joinedload(
                    Announcement.promotion
                ),
            )
        )

        limit_offset = LimitOffset(limit=limit, offset=offset)
        results, total = await self._custom_list_and_count(
            statement=stmt, limit_offset=limit_offset
        )

        favourite_announcements: list[FavouriteAnnouncement] = []

        for fav_announcement, floor_no, total_floors in results:
            if fav_announcement.announcement.apartment:
                fav_announcement.announcement.apartment.floor_no = floor_no
                fav_announcement.announcement.apartment.total_floors = total_floors
            favourite_announcements.append(fav_announcement)

        return favourite_announcements, total

    async def get_favourite_user_announcement(
        self, favourite_announcement_id: int
    ) -> FavouriteAnnouncement:
        total_floors_subquery = (
            select(
                Floor.block_id.label("block_id"),
                func.count(Floor.id).label("total_floors"),
            )
            .group_by(Floor.block_id)
            .subquery()
        )

        stmt = (
            select(
                FavouriteAnnouncement,
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
            )
            .join(
                Announcement, FavouriteAnnouncement.announcement_id == Announcement.id
            )
            .join(Apartment, Announcement.apartment_id == Apartment.id)
            .outerjoin(Floor, Apartment.floor_id == Floor.id)
            .outerjoin(Riser, Apartment.riser_id == Riser.id)
            .outerjoin(Section, Riser.section_id == Section.id)
            .outerjoin(Block, Section.block_id == Block.id)
            .outerjoin(
                total_floors_subquery, Block.id == total_floors_subquery.c.block_id
            )
            .where(FavouriteAnnouncement.id == favourite_announcement_id)
            .options(
                joinedload(FavouriteAnnouncement.announcement)
                .joinedload(Announcement.apartment)
                .selectinload(Apartment.gallery),
                joinedload(FavouriteAnnouncement.announcement)
                .joinedload(Announcement.apartment)
                .joinedload(Apartment.user)
                .joinedload(User.contact),
                joinedload(FavouriteAnnouncement.announcement).joinedload(
                    Announcement.promotion
                ),
            )
        )

        result = await self.session.execute(stmt)
        row = result.one_or_none()

        favourite_announcement, floor_no, total_floors = row

        apartment = favourite_announcement.announcement.apartment
        if apartment:
            apartment.floor_no = floor_no
            apartment.total_floors = total_floors
            apartment.contact = apartment.user.contact

        return favourite_announcement

    async def _custom_list_and_count(
        self,
        statement: Select,
        limit_offset: LimitOffset | None = None,
    ) -> tuple[Sequence[Any], int]:
        count_stmt = statement.with_only_columns(func.count())

        if limit_offset:
            statement = statement.limit(limit_offset.limit).offset(limit_offset.offset)

        result = await self.session.execute(statement)
        rows = result.all()

        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        return rows, total
