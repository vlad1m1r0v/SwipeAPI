from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse, success_response

from src.auth.dependencies import user_from_token

from src.user.services import ContactService
from src.user.schemas import GetUserSchema, GetContactSchema, UpdateContactSchema

router = APIRouter()


@router.patch(
    path="/contact",
    response_model=SuccessResponse[GetContactSchema],
    status_code=status.HTTP_200_OK,
    responses=generate_examples(auth=True, role=True, user=True),
    tags=["User: Profile"],
)
@inject
async def update_contact(
    contact_service: FromDishka[ContactService],
    data: UpdateContactSchema,
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetContactSchema]:
    result = await contact_service.update(data=data, item_id=user.contact.id)
    return success_response(
        value=contact_service.to_schema(data=result, schema_type=GetContactSchema),
        message="Contact updated successfully.",
    )
