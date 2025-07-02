from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from sqlalchemy import update

from src.user.models import Balance


class BalanceRepository(SQLAlchemyAsyncRepository[Balance]):
    model_type = Balance

    async def deposit_money(self, item_id: int, amount: float) -> None:
        stmt = (
            update(Balance)
            .where(Balance.id == item_id)
            .values(value=Balance.value + amount)
            .returning(Balance)
        )

        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()
