from typing import List, Sequence, cast

from decimal import Decimal

from dishka import AsyncContainer

from pydantic import EmailStr

from cli.schemas import (
    CreateUserSchema,
    CreateContactSchema,
    CreateComplexSchema,
    CreateInfrastructureSchema,
    CreateAdvantagesSchema,
    CreateFormalizationAndPaymentSettingsSchema,
    CreateBuildingImageSchema,
    CreateBlockSchema,
)

from cli.utils.faker import fake

from cli.contstants import (
    COMMON_PASSWORD,
    TEST_BUILDER_NAME,
    TEST_BUILDER_EMAIL,
    BUILDERS_TOTAL,
)

from cli.utils.media import save_file_from_dataset

from src.builder.enums import (
    Status,
    Type,
    Class,
    Technology,
    Territory,
    UtilityBills,
    Heating,
    Sewerage,
    WaterSupply,
    Formalization,
    BillingOptions,
    PropertyType,
    SumInContract,
)
from src.builder.schemas import (
    CreateSectionSchema,
    CreateFloorSchema,
    CreateRiserSchema,
    CreateNewsSchema,
    CreateDocumentSchema,
)
from src.builder.models import Complex, Block, Section, Floor
from src.builder.services import (
    ComplexService,
    InfrastructureService,
    FormalizationAndPaymentSettingsService,
    AdvantagesService,
    NewsService,
    GalleryService,
    DocumentService,
    BlockService,
    SectionService,
    FloorService,
    RiserService,
)

from src.user.enums import Role
from src.user.models import User
from src.user.services import UserService, ContactService


def generate_builders() -> List[CreateUserSchema]:
    photo = save_file_from_dataset(fake.building_path())
    phone = fake.ukrainian_phone()

    builders: List[CreateUserSchema] = [
        CreateUserSchema(
            name=TEST_BUILDER_NAME,
            email=cast(EmailStr, TEST_BUILDER_EMAIL),
            password=COMMON_PASSWORD,
            photo=photo,
            phone=phone,
        )
    ]

    for _ in range(BUILDERS_TOTAL):
        name = fake.unique.custom_builder_name()
        email = fake.custom_builder_email(name)
        photo = save_file_from_dataset(fake.building_path())
        phone = fake.ukrainian_phone()
        builders.append(
            CreateUserSchema(
                name=name,
                email=cast(EmailStr, email),
                password=COMMON_PASSWORD,
                photo=photo,
                phone=phone,
                role=Role.BUILDER,
            )
        )
    return builders


def generate_complexes(builders: Sequence[User]) -> List[CreateComplexSchema]:
    complexes: List[CreateComplexSchema] = []

    for builder in builders:
        complexes.append(
            CreateComplexSchema(
                user_id=builder.id,
                name=builder.name,
                address=fake.address(),
                description=fake.text(max_nb_chars=150),
                longitude=fake.longitude(),
                latitude=fake.latitude(),
            )
        )

    return complexes


def generate_contacts(builders: Sequence[User]) -> List[CreateContactSchema]:
    contacts: List[CreateContactSchema] = []

    for builder in builders:
        contacts.append(
            CreateContactSchema(
                user_id=builder.id,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.ukrainian_phone(),
                email=builder.email,
            )
        )

    return contacts


def generate_infrastructures(
    complexes: Sequence[Complex],
) -> List[CreateInfrastructureSchema]:
    infrastructures: List[CreateInfrastructureSchema] = []

    for building in complexes:
        infrastructures.append(
            CreateInfrastructureSchema(
                complex_id=building.id,
                status=fake.random_element(Status),
                type=fake.random_element(Type),
                infrastructure_class=fake.random_element(Class),
                technology=fake.random_element(Technology),
                territory=fake.random_element(Territory),
                sea_distance=Decimal(
                    str(fake.pyfloat(min_value=0.0, max_value=999.0, right_digits=3))
                ),
                utility_bills=fake.random_element(UtilityBills),
                ceiling_height=Decimal(
                    str(fake.pyfloat(min_value=2.5, max_value=4.0, right_digits=2))
                ),
                has_gas=fake.boolean(),
                heating=fake.random_element(Heating),
                sewerage=fake.random_element(Sewerage),
                water_supply=fake.random_element(WaterSupply),
            )
        )

    return infrastructures


def generate_formalization_and_payment_settings(
    complexes: Sequence[Complex],
) -> List[CreateFormalizationAndPaymentSettingsSchema]:
    settings: List[CreateFormalizationAndPaymentSettingsSchema] = []

    for building in complexes:
        settings.append(
            CreateFormalizationAndPaymentSettingsSchema(
                complex_id=building.id,
                formalization=fake.random_element(Formalization),
                billing_options=fake.random_element(BillingOptions),
                property_type=fake.random_element(PropertyType),
                sum_in_contract=fake.random_element(SumInContract),
            )
        )

    return settings


def generate_news(complexes: Sequence[Complex]) -> List[CreateNewsSchema]:
    news: List[CreateNewsSchema] = []

    for building in complexes:
        for _ in range(3):
            news.append(
                CreateNewsSchema(
                    complex_id=building.id,
                    title=fake.sentence(nb_words=5).rstrip("."),
                    description=fake.paragraph(nb_sentences=5),
                )
            )

    return news


def generate_gallery(complexes: Sequence[Complex]) -> List[CreateBuildingImageSchema]:
    images: List[CreateBuildingImageSchema] = []

    for building in complexes:
        for i in range(3):
            images.append(
                CreateBuildingImageSchema(
                    complex_id=building.id,
                    photo=save_file_from_dataset(fake.building_path()),
                    order=i + 1,
                )
            )

    return images


def generate_documents(complexes: Sequence[Complex]) -> List[CreateDocumentSchema]:
    documents: List[CreateDocumentSchema] = []

    for building in complexes:
        for _ in range(2):
            documents.append(
                CreateDocumentSchema(
                    complex_id=building.id,
                    name=fake.sentence(nb_words=5).rstrip("."),
                    file=save_file_from_dataset(fake.document_path()),
                )
            )

    return documents


def generate_advantages(complexes: Sequence[Complex]) -> List[CreateAdvantagesSchema]:
    advantages: List[CreateAdvantagesSchema] = []

    for building in complexes:
        advantages.append(
            CreateAdvantagesSchema(
                complex_id=building.id,
                has_children_playground=fake.boolean(),
                has_sports_field=fake.boolean(),
                has_parking=fake.boolean(),
                has_landscaped_area=fake.boolean(),
                has_on_site_shops=fake.boolean(),
                has_individual_heating=fake.boolean(),
                has_balcony_or_loggia=fake.boolean(),
                has_bicycle_field=fake.boolean(),
                has_panoramic_windows=fake.boolean(),
                is_close_to_sea=fake.boolean(),
                is_close_to_school=fake.boolean(),
                is_close_to_transport=fake.boolean(),
            )
        )

    return advantages


def generate_blocks(complexes: Sequence[Complex]) -> List[CreateBlockSchema]:
    blocks: List[CreateBlockSchema] = []

    for building in complexes:
        for i in range(3):
            blocks.append(CreateBlockSchema(complex_id=building.id, no=i + 1))

    return blocks


def generate_sections(blocks: Sequence[Block]) -> List[CreateSectionSchema]:
    sections: List[CreateSectionSchema] = []

    for block in blocks:
        for i in range(3):
            sections.append(CreateSectionSchema(block_id=block.id, no=i + 1))

    return sections


def generate_floors(blocks: Sequence[Block]) -> List[CreateFloorSchema]:
    floors: List[CreateFloorSchema] = []

    for block in blocks:
        for i in range(3):
            floors.append(CreateFloorSchema(block_id=block.id, no=i + 1))

    return floors


def generate_risers(sections: Sequence[Section]) -> List[CreateRiserSchema]:
    risers: List[CreateRiserSchema] = []

    for section in sections:
        for i in range(3):
            risers.append(CreateRiserSchema(section_id=section.id, no=i + 1))

    return risers


async def create_builders(
    container: AsyncContainer,
) -> tuple[Sequence[Complex], Sequence[Floor]]:
    builders_to_create = generate_builders()
    user_service = await container.get(UserService)
    builders = await user_service.create_many(builders_to_create)

    contacts_to_create = generate_contacts(builders)
    contact_service = await container.get(ContactService)
    await contact_service.create_many(contacts_to_create)

    complexes_to_create = generate_complexes(builders)
    complex_service = await container.get(ComplexService)
    complexes = await complex_service.create_many(complexes_to_create)

    infrastructures_to_create = generate_infrastructures(complexes)
    infrastructure_service = await container.get(InfrastructureService)
    await infrastructure_service.create_many(infrastructures_to_create)

    settings_to_create = generate_formalization_and_payment_settings(complexes)
    settings_service = await container.get(FormalizationAndPaymentSettingsService)
    await settings_service.create_many(settings_to_create)

    advantages_to_create = generate_advantages(complexes)
    advantages_service = await container.get(AdvantagesService)
    await advantages_service.create_many(advantages_to_create)

    news_to_create = generate_news(complexes)
    news_service = await container.get(NewsService)
    await news_service.create_many(news_to_create)

    gallery_to_create = generate_gallery(complexes)
    gallery_service = await container.get(GalleryService)
    await gallery_service.create_many(gallery_to_create)

    documents_to_create = generate_documents(complexes)
    document_service = await container.get(DocumentService)
    await document_service.create_many(documents_to_create)

    blocks_to_create = generate_blocks(complexes)
    block_service = await container.get(BlockService)
    blocks = await block_service.create_many(blocks_to_create)

    sections_to_create = generate_sections(blocks)
    section_service = await container.get(SectionService)
    sections = await section_service.create_many(sections_to_create)

    floors_to_create = generate_floors(blocks)
    floor_service = await container.get(FloorService)
    floors = await floor_service.create_many(floors_to_create)

    risers_to_create = generate_risers(sections)
    riser_service = await container.get(RiserService)
    await riser_service.create_many(risers_to_create)

    return complexes, floors
