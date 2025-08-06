from typing import Sequence, Any

from sqlalchemy.orm import joinedload
from sqlalchemy import select, func, Select

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset

from src.announcements.models import (
    Announcement,
    Promotion,
    FavouriteAnnouncement,
    AnnouncementView,
    Complaint,
)

from src.apartments.models import Apartment

from src.buildings.models import Block, Floor, Section, Riser

from src.user.models import User


class AnnouncementRepository(SQLAlchemyAsyncRepository[Announcement]):
    model_type = Announcement

    async def create_announcement(self, data: dict) -> Announcement:
        created = await self.add(Announcement(**data))

        self.session.add(Promotion(announcement_id=created.id))
        await self.session.commit()

        return created

    async def get_announcements_for_user(
        self, user_id: int, limit: int, offset: int
    ) -> tuple[Sequence[Announcement], int]:
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
                Announcement,
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
            )
            .join(Apartment, Announcement.apartment_id == Apartment.id)
            .outerjoin(Floor, Apartment.floor_id == Floor.id)
            .outerjoin(Riser, Apartment.riser_id == Riser.id)
            .outerjoin(Section, Riser.section_id == Section.id)
            .outerjoin(Block, Section.block_id == Block.id)
            .outerjoin(
                total_floors_subquery, Block.id == total_floors_subquery.c.block_id
            )
            .where(Apartment.user_id == user_id)
            .options(
                joinedload(Announcement.apartment).selectinload(Apartment.gallery),
                joinedload(Announcement.promotion),
            )
        )

        limit_offset = LimitOffset(limit=limit, offset=offset)
        results, total = await self._custom_list_and_count(
            statement=stmt, limit_offset=limit_offset
        )

        announcements: list[Announcement] = []
        for announcement, floor_no, total_floors in results:
            announcement.apartment.floor_no = floor_no
            announcement.apartment.total_floors = total_floors
            announcements.append(announcement)

        return announcements, total

    async def get_announcements_for_admin(
        self, limit: int, offset: int
    ) -> tuple[Sequence[Announcement], int]:
        total_floors_subquery = (
            select(
                Floor.block_id.label("block_id"),
                func.count(Floor.id).label("total_floors"),
            )
            .group_by(Floor.block_id)
            .subquery()
        )

        complained_announcements_subquery = (
            select(Complaint.announcement_id).distinct().subquery()
        )

        stmt = (
            select(
                Announcement,
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
            )
            .join(Apartment, Announcement.apartment_id == Apartment.id)
            .outerjoin(Floor, Apartment.floor_id == Floor.id)
            .outerjoin(Riser, Apartment.riser_id == Riser.id)
            .outerjoin(Section, Riser.section_id == Section.id)
            .outerjoin(Block, Section.block_id == Block.id)
            .outerjoin(
                total_floors_subquery, Block.id == total_floors_subquery.c.block_id
            )
            .outerjoin(
                complained_announcements_subquery,
                Announcement.id == complained_announcements_subquery.c.announcement_id,
            )
            .where(
                complained_announcements_subquery.c.announcement_id.is_(None)
            )  # Без скарг
            .options(
                joinedload(Announcement.apartment).selectinload(Apartment.gallery),
                joinedload(Announcement.promotion),
            )
        )

        limit_offset = LimitOffset(limit=limit, offset=offset)
        results, total = await self._custom_list_and_count(
            statement=stmt, limit_offset=limit_offset
        )

        announcements: list[Announcement] = []
        for announcement, floor_no, total_floors in results:
            announcement.apartment.floor_no = floor_no
            announcement.apartment.total_floors = total_floors
            announcements.append(announcement)

        return announcements, total

    async def get_announcement_detail_for_shared(
        self, user_id: int, announcement_id: int
    ) -> Announcement:
        self.session.add(
            AnnouncementView(user_id=user_id, announcement_id=announcement_id)
        )
        await self.session.commit()

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
                Announcement,
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
            )
            .join(Apartment, Announcement.apartment_id == Apartment.id)
            .outerjoin(Floor, Apartment.floor_id == Floor.id)
            .outerjoin(Riser, Apartment.riser_id == Riser.id)
            .outerjoin(Section, Riser.section_id == Section.id)
            .outerjoin(Block, Section.block_id == Block.id)
            .outerjoin(
                total_floors_subquery, Block.id == total_floors_subquery.c.block_id
            )
            .where(Announcement.id == announcement_id)
            .options(
                joinedload(Announcement.promotion),
                joinedload(Announcement.apartment).selectinload(Apartment.gallery),
                joinedload(Announcement.apartment)
                .joinedload(Apartment.user)
                .joinedload(User.contact),
            )
        )

        result = await self.session.execute(stmt)
        row = result.one_or_none()

        announcement, floor_no, total_floors = row

        apartment = announcement.apartment
        apartment.floor_no = floor_no
        apartment.total_floors = total_floors
        apartment.contact = apartment.user.contact

        return announcement

    async def get_announcement_detail_for_user(
        self, announcement_id: int
    ) -> Announcement:
        total_floors_subquery = (
            select(
                Floor.block_id.label("block_id"),
                func.count(Floor.id).label("total_floors"),
            )
            .group_by(Floor.block_id)
            .subquery()
        )

        views_count_subquery = (
            select(AnnouncementView.announcement_id, func.count().label("views_count"))
            .group_by(AnnouncementView.announcement_id)
            .subquery()
        )

        favourites_count_subq = (
            select(
                FavouriteAnnouncement.announcement_id,
                func.count().label("favourites_count"),
            )
            .group_by(FavouriteAnnouncement.announcement_id)
            .subquery()
        )

        stmt = (
            select(
                Announcement,
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
                views_count_subquery.c.views_count,
                favourites_count_subq.c.favourites_count,
            )
            .join(Apartment, Announcement.apartment_id == Apartment.id)
            .outerjoin(Floor, Apartment.floor_id == Floor.id)
            .outerjoin(Riser, Apartment.riser_id == Riser.id)
            .outerjoin(Section, Riser.section_id == Section.id)
            .outerjoin(Block, Section.block_id == Block.id)
            .outerjoin(
                total_floors_subquery, Block.id == total_floors_subquery.c.block_id
            )
            .outerjoin(
                views_count_subquery,
                views_count_subquery.c.announcement_id == Announcement.id,
            )
            .outerjoin(
                favourites_count_subq,
                favourites_count_subq.c.announcement_id == Announcement.id,
            )
            .where(Announcement.id == announcement_id)
            .options(
                joinedload(Announcement.promotion),
                joinedload(Announcement.apartment).selectinload(Apartment.gallery),
                joinedload(Announcement.apartment)
                .joinedload(Apartment.user)
                .joinedload(User.contact),
            )
        )

        result = await self.session.execute(stmt)
        row = result.one_or_none()

        announcement, floor_no, total_floors, views_count, favourites_count = row

        apartment = announcement.apartment
        apartment.floor_no = floor_no
        apartment.total_floors = total_floors
        apartment.contact = apartment.user.contact

        setattr(announcement, "views_count", views_count or 0)
        setattr(announcement, "favourites_count", favourites_count or 0)

        return announcement

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
