from fastapi import APIRouter, Depends

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import builder_from_token

from src.builder.schemas import GetBuilderSchema

router = APIRouter()


@router.get(
    path="/profile",
    response_model=SuccessResponse[GetBuilderSchema],
    responses=generate_examples(auth=True, role=True),
    tags=["Builder: Profile"],
)
def get_profile(
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetBuilderSchema]:
    return SuccessResponse(data=builder)
