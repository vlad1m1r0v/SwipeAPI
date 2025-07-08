from fastapi import APIRouter, Depends

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

router = APIRouter()


@router.get(
    path="/profile",
    response_model=SuccessResponse[GetUserSchema],
    responses=generate_examples(auth=True, user=True, role=True),
    tags=["User: Profile"],
)
def get_profile(
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetUserSchema]:
    return SuccessResponse(data=user)
