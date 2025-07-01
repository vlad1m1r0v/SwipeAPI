from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Request, Depends

from src.core.schemas import MediaItem

from src.auth.dependencies import builder_from_token

from src.builder.services import GalleryService
from src.builder.schemas import GetBuilderSchema

from src.user.services import UserService

router = APIRouter()


@router.patch("/gallery", tags=["Builder: Gallery"])
@inject
async def update_gallery(
    request: Request,
    gallery_service: FromDishka[GalleryService],
    user_service: FromDishka[UserService],
    media_set: List[MediaItem],
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    await gallery_service.update_gallery(
        complex_id=builder.complex.id, request=request, media_set=media_set
    )
    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)
