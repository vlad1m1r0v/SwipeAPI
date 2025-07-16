from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Body
from starlette import status

from src.core.exceptions import IntegrityErrorException
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.apartments.services import AddToComplexRequestService
from src.apartments.schemas import CreateAddToComplexRequest, GetAddToComplexRequest

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

router = APIRouter(
    prefix="/add-to-complex-request", tags=["User: Add to complex requests"]
)


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        IntegrityErrorException, auth=True, role=True, user=True
    ),
    response_model=SuccessResponse[GetAddToComplexRequest],
)
@inject
async def create_add_to_complex_request(
    add_to_complex_request_service: FromDishka[AddToComplexRequestService],
    data: CreateAddToComplexRequest = Body(),
    _: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetAddToComplexRequest]:
    created = await add_to_complex_request_service.create(data=data.model_dump())
    return SuccessResponse(
        data=add_to_complex_request_service.to_schema(
            data=created, schema_type=GetAddToComplexRequest
        )
    )
