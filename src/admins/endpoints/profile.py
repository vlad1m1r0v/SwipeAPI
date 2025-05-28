from fastapi import (
    APIRouter,
    Depends
)

from src.auth.dependencies import admin_from_token

from src.admins.schemas import GetAdminSchema

router = APIRouter()


@router.get("/profile")
def get_profile(
        admin: GetAdminSchema = Depends(admin_from_token)
) -> GetAdminSchema:
    return admin