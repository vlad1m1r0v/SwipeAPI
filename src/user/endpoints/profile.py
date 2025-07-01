from fastapi import APIRouter, Depends

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

router = APIRouter()


@router.get("/profile", tags=["User: Profile"])
def get_profile(user: GetUserSchema = Depends(user_from_token)) -> GetUserSchema:
    return user
