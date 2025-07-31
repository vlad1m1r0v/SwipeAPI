from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.buildings.schemas.grid import GetFloorGridSchema
from src.buildings.models import Section, Floor, Riser

from src.apartments.models import Apartment


class GridRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_layout(self, section_id: int) -> List[GetFloorGridSchema]:
        section = await self._session.get(Section, section_id)

        floors_stmt = (
            select(Floor)
            .where(Floor.block_id == section.block_id)
            .order_by(Floor.no.asc())
        )
        floors = (await self._session.execute(floors_stmt)).scalars().all()

        risers_stmt = (
            select(Riser).where(Riser.section_id == section_id).order_by(Riser.no.asc())
        )
        risers = (await self._session.execute(risers_stmt)).scalars().all()

        flats_stmt = select(Apartment.id, Apartment.floor_id, Apartment.riser_id).where(
            Apartment.floor_id.in_([f.id for f in floors]),
            Apartment.riser_id.in_([r.id for r in risers]),
        )
        flats = await self._session.execute(flats_stmt)

        flat_map = {
            (floor_id, riser_id): flat_id for flat_id, floor_id, riser_id in flats.all()
        }

        result = []
        for floor in floors:
            risers_list = []
            for riser in risers:
                flat_id = flat_map.get((floor.id, riser.id))
                risers_list.append(
                    {"riser_id": riser.id, "riser_no": riser.no, "flat_id": flat_id}
                )
            result.append(
                {"floor_id": floor.id, "floor_no": floor.no, "risers": risers_list}
            )

        return result
