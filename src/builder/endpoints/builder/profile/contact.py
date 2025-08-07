from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.builder.schemas import GetBuilderSchema

from src.auth.dependencies import builder_from_token

from src.user.services import ContactService
from src.user.schemas import GetContactSchema, UpdateContactSchema

router = APIRouter()


@router.patch(
    path="/contact",
    response_model=SuccessResponse[GetContactSchema],
    status_code=status.HTTP_200_OK,
    responses=generate_examples(auth=True, role=True),
    response_model_exclude_none=True,
)
@inject
async def update_contact(
    contact_service: FromDishka[ContactService],
    data: UpdateContactSchema,
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetContactSchema]:
    result = await contact_service.update(data=data, item_id=builder.contact.id)
    return SuccessResponse(
        data=contact_service.to_schema(data=result, schema_type=GetContactSchema),
    )
