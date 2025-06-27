from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query, Body

from advanced_alchemy.service import OffsetPagination

from src.core.schemas import SuccessfulMessageSchema

from src.builders.schemas import (
    GetBuilderSchema,
    GetSectionSchema,
    UpdateSectionSchema,
    CreateSectionSchema,
)
from src.builders.services import SectionService
from src.builders.dependencies import check_builder_owns_section

from src.auth.dependencies import builder_from_token

router = APIRouter(prefix="/sections", tags=["Builders: Sections"])


@router.get("", response_model=OffsetPagination[GetSectionSchema])
@inject
async def get_sections(
    section_service: FromDishka[SectionService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    block_id: int | None = Query(default=None),
    no: int | None = Query(default=None),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> OffsetPagination[GetSectionSchema]:
    results, total = await section_service.get_sections(
        limit=limit,
        offset=offset,
        complex_id=builder.complex.id,
        block_id=block_id,
        no=no,
    )
    return section_service.to_schema(
        data=results, total=total, schema_type=GetSectionSchema
    )


@router.post("", response_model=SuccessfulMessageSchema)
@inject
async def create_section(
    section_service: FromDishka[SectionService],
    data: CreateSectionSchema = Body(),
    _: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessfulMessageSchema:
    await section_service.create(data=data.model_dump())
    return SuccessfulMessageSchema(
        message="Section has been added successfully to block."
    )


@router.patch("/{section_id}", response_model=SuccessfulMessageSchema)
@inject
async def update_section(
    section_service: FromDishka[SectionService],
    section_id: int,
    data: UpdateSectionSchema = Body(),
    _: GetBuilderSchema = Depends(check_builder_owns_section),
) -> SuccessfulMessageSchema:
    await section_service.update(
        item_id=section_id, data=data.model_dump(exclude_none=True)
    )
    return SuccessfulMessageSchema(message="Section has been updated successfully.")


@router.delete("/{section_id}", response_model=SuccessfulMessageSchema)
@inject
async def delete_section(
    section_service: FromDishka[SectionService],
    section_id: int,
    _: GetBuilderSchema = Depends(check_builder_owns_section),
):
    await section_service.delete(item_id=section_id)
    return SuccessfulMessageSchema(message="Section has been deleted successfully.")
