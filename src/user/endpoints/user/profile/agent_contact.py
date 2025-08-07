from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import user_from_token

from src.user.services import AgentContactService
from src.user.schemas import (
    GetUserSchema,
    GetAgentContactSchema,
    UpdateAgentContactSchema,
)

router = APIRouter()


@router.patch(
    path="/agent-contact",
    response_model=SuccessResponse[GetAgentContactSchema],
    status_code=status.HTTP_200_OK,
    responses=generate_examples(auth=True, role=True, user=True),
    response_model_exclude_none=True,
)
@inject
async def update_agent_contact(
    agent_contact_service: FromDishka[AgentContactService],
    data: UpdateAgentContactSchema,
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetAgentContactSchema]:
    result = await agent_contact_service.update(
        data=data, item_id=user.agent_contact.id
    )
    return SuccessResponse(
        data=agent_contact_service.to_schema(
            data=result, schema_type=GetAgentContactSchema
        )
    )
