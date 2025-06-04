from fastapi import APIRouter, Depends

from src.auth.dependencies import builder_from_token

from src.builders.schemas import GetBuilderSchema

router = APIRouter()


@router.get("/profile")
def get_profile(
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    return builder
