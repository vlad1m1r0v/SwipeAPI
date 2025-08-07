from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.exceptions import (
    DuplicateKeyException,
    IsNotOwnerException,
    IntegrityErrorException,
    NotFoundException,
)
from src.core.schemas import SuccessResponse
from src.core.utils import generate_examples

from src.auth.dependencies import builder_from_token

from src.builder.services import FormalizationAndPaymentSettingsService
from src.builder.schemas import (
    UpdateFormalizationAndPaymentSettingsSchema,
    GetFormalizationAndPaymentSettingsSchema,
    GetBuilderSchema,
)

router = APIRouter()


@router.patch(
    path="/formalization-and-payment-settings",
    response_model=SuccessResponse[GetFormalizationAndPaymentSettingsSchema],
    responses=generate_examples(
        DuplicateKeyException,
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def update_formalization_and_payment_settings(
    formalization_and_payment_settings_service: FromDishka[
        FormalizationAndPaymentSettingsService
    ],
    data: UpdateFormalizationAndPaymentSettingsSchema,
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetFormalizationAndPaymentSettingsSchema]:
    data = await formalization_and_payment_settings_service.update(
        data=data, item_id=builder.complex.formalization_and_payment_settings.id
    )
    return SuccessResponse(
        data=formalization_and_payment_settings_service.to_schema(
            data=data, schema_type=GetFormalizationAndPaymentSettingsSchema
        ),
    )
