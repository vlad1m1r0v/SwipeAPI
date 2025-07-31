from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.buildings.repositories import GridRepository
from src.buildings.schemas.grid import GetFloorGridSchema


class GridService:
    def __init__(self, session: AsyncSession):
        self.repo = GridRepository(session=session)

    async def get_layout(self, section_id: int) -> List[GetFloorGridSchema]:
        return await self.repo.get_layout(section_id)
