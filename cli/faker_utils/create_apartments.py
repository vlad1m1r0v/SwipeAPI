from itertools import product
from typing import Sequence, List
from collections import defaultdict

from dishka import AsyncContainer

from sqlalchemy import orm

from .faker_instance import fake
from .media_utils import save_file_from_dataset

from src.apartments.models import Apartment
from src.apartments.schemas import CreateApartmentWithUserSchema, CreateImageSchema
from src.apartments.services import ApartmentService, ApartmentGalleryService
from src.apartments.enums import (
    OwnershipType,
    Bedrooms,
    Bathrooms,
    Commission,
    ApartmentCondition,
    Finishing,
    Rooms,
    CallMethod,
)

from src.builder.enums import Technology, PropertyType, Heating
from src.builder.models import Floor, Riser
from src.builder.services import RiserService

from src.user.models import User


def generate_apartments(
    users: Sequence[User], floors: Sequence[Floor], risers: Sequence[Riser]
) -> List[CreateApartmentWithUserSchema]:
    apartments: List[CreateApartmentWithUserSchema] = []

    floors_by_block = defaultdict(list)
    risers_by_block = defaultdict(list)

    for floor in floors:
        floors_by_block[floor.block_id].append(floor)

    for riser in risers:
        risers_by_block[riser.section.block_id].append(riser)

    for block_id in set(floors_by_block) & set(risers_by_block):
        block_floors = floors_by_block[block_id]
        block_risers = risers_by_block[block_id]

        for i, (floor, riser) in enumerate(product(block_floors, block_risers)):
            apartments.append(
                CreateApartmentWithUserSchema(
                    user_id=users[i % len(users)].id,
                    floor_id=floor.id,
                    riser_id=riser.id,
                    address=fake.street_address(),
                    district=fake.city(),
                    microdistrict=fake.street_name(),
                    longitude=fake.longitude(),
                    latitude=fake.latitude(),
                    technology=fake.enum(Technology),
                    ownership_type=fake.enum(OwnershipType),
                    property_type=fake.enum(PropertyType),
                    bedrooms=fake.enum(Bedrooms),
                    bathrooms=fake.enum(Bathrooms),
                    kitchen_area=fake.pydecimal(
                        min_value=6, max_value=20, right_digits=1
                    ),
                    heating=fake.enum(Heating),
                    has_balcony_or_loggia=fake.boolean(),
                    has_mortgage=fake.boolean(),
                    commission_to_agent=fake.enum(Commission),
                    condition=fake.enum(ApartmentCondition),
                    finishing=fake.enum(Finishing),
                    rooms=fake.enum(Rooms),
                    area=fake.pydecimal(min_value=30, max_value=150, right_digits=1),
                    call_method=fake.enum(CallMethod),
                    description=fake.paragraph(nb_sentences=3),
                    price=fake.random_int(min=30000, max=200000),
                    scheme=save_file_from_dataset(fake.scheme_path()),
                    gallery=[],
                )
            )

    return apartments


def generate_gallery(apartments: Sequence[Apartment]) -> List[CreateImageSchema]:
    gallery: List[CreateImageSchema] = []

    for apartment in apartments:
        for i in range(3):
            gallery.append(
                CreateImageSchema(
                    apartment_id=apartment.id,
                    photo=save_file_from_dataset(fake.room_path()),
                    order=i + 1,
                )
            )

    return gallery


async def create_apartments(
    container: AsyncContainer,
    users: Sequence[User],
    floors: Sequence[Floor],
) -> Sequence[Apartment]:
    riser_service = await container.get(RiserService)
    risers = await riser_service.list(load=[orm.joinedload(Riser.section)])

    apartments_to_create = generate_apartments(users, floors, risers)
    apartments_service = await container.get(ApartmentService)
    apartments = await apartments_service.create_many(apartments_to_create)

    gallery_to_create = generate_gallery(apartments)
    gallery_service = await container.get(ApartmentGalleryService)
    await gallery_service.create_many(gallery_to_create)

    return apartments
