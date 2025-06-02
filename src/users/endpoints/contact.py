from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Form

from src.auth.dependencies import user_from_token

from src.users.services import UserService, ContactService
from src.users.schemas import GetUserSchema, UpdateContactSchema

router = APIRouter()


@router.patch("/contact")
@inject
async def update_contact(
    contact_service: FromDishka[ContactService],
    user_service: FromDishka[UserService],
    data: Annotated[UpdateContactSchema, Form()],
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    await contact_service.update(data=data, item_id=user.contact.id)
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)
