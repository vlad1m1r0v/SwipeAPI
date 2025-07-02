from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.user.models import Balance
from src.user.repositories import BalanceRepository


class BalanceService(SQLAlchemyAsyncRepositoryService[Balance, BalanceRepository]):
    repository_type = BalanceRepository

    async def deposit_money(self, item_id: int, amount: float) -> Balance:
        return await self.repository.deposit_money(item_id, amount)
