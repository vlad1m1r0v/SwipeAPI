from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends

from src.auth.dependencies import builder_from_token

from src.builder.services import FormalizationAndPaymentSettingsService
from src.builder.schemas import (
    UpdateFormalizationAndPaymentSettingsSchema,
    GetBuilderSchema,
)

from src.user.services import UserService

router = APIRouter()


@router.patch("/formalization-and-payment", tags=["Builder: Profile"])
@inject
async def update_formalization_and_payment_settings(
    formalization_and_payment_settings_service: FromDishka[
        FormalizationAndPaymentSettingsService
    ],
    user_service: FromDishka[UserService],
    data: UpdateFormalizationAndPaymentSettingsSchema,
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    await formalization_and_payment_settings_service.update(
        data=data, item_id=builder.complex.formalization_and_payment_settings.id
    )
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)
