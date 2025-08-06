from typing import Sequence, Any

from sqlalchemy.orm import joinedload, aliased
from sqlalchemy import select, func, Select

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset

from src.announcements.models import Complaint, Announcement

from src.apartments.models import Apartment

from src.buildings.models import Block, Floor, Section, Riser


class AnnouncementComplaintRepository(SQLAlchemyAsyncRepository[Complaint]):
    model_type = Complaint

    async def get_admin_complaints(
        self, limit: int, offset: int, admin_id: int
    ) -> tuple[list[Complaint], int]:
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
                Complaint,
                Floor.no.label("floor_no"),
                total_floors_subquery.c.total_floors,
            )
            .join(Announcement, Complaint.announcement_id == Announcement.id)
            .join(Apartment, Announcement.apartment_id == Apartment.id)
            .outerjoin(Floor, Apartment.floor_id == Floor.id)
            .outerjoin(Riser, Apartment.riser_id == Riser.id)
            .outerjoin(Section, Riser.section_id == Section.id)
            .outerjoin(Block, Section.block_id == Block.id)
            .outerjoin(
                total_floors_subquery, Block.id == total_floors_subquery.c.block_id
            )
            .where(Complaint.user_id == admin_id)
            .options(
                joinedload(Complaint.announcement)
                .joinedload(Announcement.apartment)
                .selectinload(Apartment.gallery),
                joinedload(Complaint.announcement).joinedload(Announcement.promotion),
            )
        )

        limit_offset = LimitOffset(limit=limit, offset=offset)
        results, total = await self._custom_list_and_count(
            statement=stmt, limit_offset=limit_offset
        )

        complaints: list[Complaint] = []

        for complaint, floor_no, total_floors in results:
            if complaint.announcement.apartment:
                complaint.announcement.apartment.floor_no = floor_no
                complaint.announcement.apartment.total_floors = total_floors
            complaints.append(complaint)

        return complaints, total

    async def get_complaint(self, complaint_id: int) -> Complaint:
        apartment_alias = aliased(Apartment)

        subquery_total_floors = (
            select(
                Apartment.riser_id,
                func.count(func.distinct(Apartment.floor_id)).label("total_floors"),
            )
            .group_by(Apartment.riser_id)
            .subquery()
        )

        subquery_floor_no = select(
            apartment_alias.riser_id,
            apartment_alias.floor_id,
            func.row_number()
            .over(
                partition_by=apartment_alias.riser_id, order_by=apartment_alias.floor_id
            )
            .label("floor_no"),
        ).subquery()

        stmt = (
            select(
                Complaint,
                subquery_floor_no.c.floor_no,
                subquery_total_floors.c.total_floors,
            )
            .join(Announcement, Complaint.announcement_id == Announcement.id)
            .join(Apartment, Announcement.apartment_id == Apartment.id)
            .join(
                subquery_floor_no,
                (subquery_floor_no.c.riser_id == Apartment.riser_id)
                & (subquery_floor_no.c.floor_id == Apartment.floor_id),
            )
            .join(
                subquery_total_floors,
                subquery_total_floors.c.riser_id == Apartment.riser_id,
            )
            .where(Complaint.id == complaint_id)
            .options(
                joinedload(Complaint.announcement)
                .joinedload(Announcement.apartment)
                .selectinload(Apartment.gallery),
                joinedload(Complaint.announcement).joinedload(Announcement.promotion),
            )
        )

        result = await self.session.execute(stmt)
        row = result.one_or_none()

        complaint, floor_no, total_floors = row
        complaint.announcement.apartment.floor_no = floor_no
        complaint.announcement.apartment.total_floors = total_floors
        return complaint

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
