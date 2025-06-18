from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Request, Depends, UploadFile, File

from src.core.utils import save_file

from src.auth.dependencies import builder_from_token

from src.builders.services import GalleryService
from src.builders.schemas import GetBuilderSchema, CreateGalleryImageSchema

from src.users.services import UserService

router = APIRouter()


@router.patch("/gallery")
@inject
async def update_gallery(
    request: Request,
    gallery_service: FromDishka[GalleryService],
    user_service: FromDishka[UserService],
    images: List[UploadFile] = File(),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> GetBuilderSchema:
    new_images = []

    for image in images:
        new_images.append(
            CreateGalleryImageSchema(
                complex_id=builder.complex.id,
                photo=save_file(request=request, file=image),
            )
        )

    await gallery_service.update_gallery(
        complex_id=builder.complex.id, images=new_images
    )

    profile = await user_service.get_builder_profile(item_id=builder.id)
    return user_service.to_schema(data=profile, schema_type=GetBuilderSchema)
