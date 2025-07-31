from fastapi import APIRouter, Depends
from starlette import status

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import admin_from_token

from src.admin.schemas import GetAdminSchema

router = APIRouter()


@router.get(
    path="/profile",
    response_model=SuccessResponse[GetAdminSchema],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
    tags=["Admin: Profile"],
)
def get_profile(
    admin: GetAdminSchema = Depends(admin_from_token),
) -> SuccessResponse[GetAdminSchema]:
    return SuccessResponse(data=admin)
