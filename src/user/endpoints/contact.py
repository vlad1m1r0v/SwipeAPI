from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends

from src.auth.dependencies import user_from_token

from src.user.services import UserService, ContactService
from src.user.schemas import GetUserSchema, UpdateContactSchema

router = APIRouter()


@router.patch(path="/contact", tags=["User: Profile"])
@inject
async def update_contact(
    contact_service: FromDishka[ContactService],
    user_service: FromDishka[UserService],
    data: UpdateContactSchema,
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    await contact_service.update(data=data, item_id=user.contact.id)
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)
