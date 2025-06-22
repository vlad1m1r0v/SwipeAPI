from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends

from src.auth.dependencies import user_from_token

from src.users.services import UserService, AgentContactService
from src.users.schemas import GetUserSchema, UpdateAgentContactSchema

router = APIRouter()


@router.patch(
    path="/agent-contact", response_model=GetUserSchema, tags=["Users: Profile"]
)
@inject
async def update_agent_contact(
    agent_contact_service: FromDishka[AgentContactService],
    user_service: FromDishka[UserService],
    data: UpdateAgentContactSchema,
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    await agent_contact_service.update(data=data, item_id=user.contact.id)
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)
