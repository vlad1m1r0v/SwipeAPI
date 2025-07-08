from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import user_from_token

from src.user.services import BalanceService
from src.user.schemas import GetUserSchema, GetBalanceSchema, DepositBalanceSchema

router = APIRouter()


@router.post(
    path="/balance/deposit",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse[GetBalanceSchema],
    responses=generate_examples(auth=True, role=True, user=True),
    tags=["User: Balance"],
)
@inject
async def deposit_money(
    data: DepositBalanceSchema,
    balance_service: FromDishka[BalanceService],
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetBalanceSchema]:
    result = await balance_service.deposit_money(
        item_id=user.balance.id, amount=data.amount
    )
    return SuccessResponse(
        data=balance_service.to_schema(data=result, schema_type=GetBalanceSchema)
    )
