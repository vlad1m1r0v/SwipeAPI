from decimal import Decimal

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.users.exceptions import BalanceNotFoundException
from src.users.models import Balance
from src.users.repositories import BalanceRepository


class BalanceService(
    SQLAlchemyAsyncRepositoryService[Balance, BalanceRepository]
):
    repository_type = BalanceRepository

    async def deposit_money(self, item_id: int, amount: float) -> None:
        balance = await self.get_one_or_none(id=item_id)

        if not balance:
            raise BalanceNotFoundException()

        await self.update(
            data={'value': balance.value + Decimal(amount)},
            item_id=item_id
        )