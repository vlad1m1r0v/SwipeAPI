from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query, Body
from starlette import status

from advanced_alchemy.service import OffsetPagination

from src.core.exceptions import (
    IsNotOwnerException,
    IntegrityErrorException,
    NotFoundException,
    DuplicateKeyException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.builder.schemas import (
    GetBuilderSchema,
    GetSectionSchema,
    GetSectionWithComplexSchema,
    UpdateSectionSchema,
    CreateSectionSchema,
)
from src.builder.services import SectionService
from src.builder.dependencies import check_builder_owns_section

from src.auth.dependencies import builder_from_token, user_from_token

from src.user.schemas import GetUserSchema

router = APIRouter(prefix="/sections", tags=["Builder: Sections"])

sections = APIRouter(
    prefix="/add-to-complex-request/sections", tags=["User: Add to complex requests"]
)


@sections.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetSectionWithComplexSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_sections(
    section_service: FromDishka[SectionService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    complex_id: int | None = Query(default=None),
    block_id: int | None = Query(default=None),
    no: int | None = Query(default=None),
    _: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetSectionWithComplexSchema]]:
    results, total = await section_service.get_sections(
        limit=limit,
        offset=offset,
        complex_id=complex_id,
        block_id=block_id,
        no=no,
    )
    return SuccessResponse(
        data=section_service.to_schema(
            data=results, total=total, schema_type=GetSectionWithComplexSchema
        )
    )


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetSectionSchema]],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_complex_sections(
    section_service: FromDishka[SectionService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    block_id: int | None = Query(default=None),
    no: int | None = Query(default=None),
    builder: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[OffsetPagination[GetSectionSchema]]:
    results, total = await section_service.get_sections(
        limit=limit,
        offset=offset,
        complex_id=builder.complex.id,
        block_id=block_id,
        no=no,
    )
    return SuccessResponse(
        data=section_service.to_schema(
            data=results, total=total, schema_type=GetSectionSchema
        )
    )


@router.post(
    path="",
    response_model=SuccessResponse[GetSectionSchema],
    responses=generate_examples(IntegrityErrorException, auth=True, role=True),
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_section(
    section_service: FromDishka[SectionService],
    data: CreateSectionSchema = Body(),
    _: GetBuilderSchema = Depends(builder_from_token),
) -> SuccessResponse[GetSectionSchema]:
    created = await section_service.create(data=data.model_dump())
    section = await section_service.get_section(item_id=created.id)
    return SuccessResponse(
        data=section_service.to_schema(data=section, schema_type=GetSectionSchema)
    )


@router.patch(
    path="/{section_id}",
    response_model=SuccessResponse[GetSectionSchema],
    responses=generate_examples(
        DuplicateKeyException,
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
)
@inject
async def update_section(
    section_service: FromDishka[SectionService],
    section_id: int,
    data: UpdateSectionSchema = Body(),
    _: GetBuilderSchema = Depends(check_builder_owns_section),
) -> SuccessResponse[GetSectionSchema]:
    updated = await section_service.update(
        item_id=section_id, data=data.model_dump(exclude_none=True)
    )
    section = await section_service.get_section(item_id=updated.id)
    return SuccessResponse(
        data=section_service.to_schema(data=section, schema_type=GetSectionSchema)
    )


@router.delete(
    path="/{section_id}",
    response_model=SuccessResponse,
    responses=generate_examples(
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
    ),
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_section(
    section_service: FromDishka[SectionService],
    section_id: int,
    _: GetBuilderSchema = Depends(check_builder_owns_section),
) -> SuccessResponse:
    await section_service.delete(item_id=section_id)
    return SuccessResponse(message="Section has been deleted successfully.")
