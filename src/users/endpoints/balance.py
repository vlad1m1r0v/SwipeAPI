from typing import Annotated

from pydantic import conint

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Form

from src.auth.dependencies import user_from_token

from src.users.services import UserService, BalanceService
from src.users.schemas import GetUserSchema

router = APIRouter()


@router.post("/balance/deposit")
@inject
async def deposit_money(
    amount: Annotated[conint(le=9999), Form()],
    user_service: FromDishka[UserService],
    balance_service: FromDishka[BalanceService],
    user: GetUserSchema = Depends(user_from_token),
):
    await balance_service.deposit_money(item_id=user.balance.id, amount=amount)
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)
