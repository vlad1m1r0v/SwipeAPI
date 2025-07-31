from itertools import product
from typing import Sequence, List
from collections import defaultdict

from dishka import AsyncContainer

from sqlalchemy import orm

from cli.utils.faker import fake
from cli.utils.media import save_file_from_dataset

from cli.schemas import CreateApartmentSchema, CreateApartmentImageSchema

from src.apartments.models import Apartment
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

from src.buildings.models import Floor, Riser
from src.buildings.services import RiserService

from src.requests.schemas import CreateAddToComplexRequest
from src.requests.services import AddToComplexRequestService

from src.user.models import User


def generate_apartments(
    users: Sequence[User], floors: Sequence[Floor], risers: Sequence[Riser]
) -> tuple[
    List[CreateApartmentSchema], List[CreateApartmentSchema], list[tuple[int, int]]
]:
    linked_apartments: List[CreateApartmentSchema] = []

    orphan_apartments: List[CreateApartmentSchema] = []
    free_places: list[tuple[int, int]] = []

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
            if i % 2:
                linked_apartments.append(
                    CreateApartmentSchema(
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
                        area=fake.pydecimal(
                            min_value=30, max_value=150, right_digits=1
                        ),
                        call_method=fake.enum(CallMethod),
                        description=fake.paragraph(nb_sentences=3),
                        price=fake.random_int(min=30000, max=200000),
                        scheme=save_file_from_dataset(fake.scheme_path()),
                        gallery=[],
                    )
                )
            else:
                orphan_apartments.append(
                    CreateApartmentSchema(
                        user_id=users[i % len(users)].id,
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
                        area=fake.pydecimal(
                            min_value=30, max_value=150, right_digits=1
                        ),
                        call_method=fake.enum(CallMethod),
                        description=fake.paragraph(nb_sentences=3),
                        price=fake.random_int(min=30000, max=200000),
                        scheme=save_file_from_dataset(fake.scheme_path()),
                        gallery=[],
                    )
                )

                free_places.append((floor.id, riser.id))

    return linked_apartments, orphan_apartments, free_places


def generate_gallery(
    apartments: Sequence[Apartment],
) -> List[CreateApartmentImageSchema]:
    gallery: List[CreateApartmentImageSchema] = []

    for apartment in apartments:
        for i in range(3):
            gallery.append(
                CreateApartmentImageSchema(
                    apartment_id=apartment.id,
                    photo=save_file_from_dataset(fake.room_path()),
                    order=i + 1,
                )
            )

    return gallery


def generate_requests(
    apartments: Sequence[Apartment], free_places: list[tuple[int, int]]
) -> List[CreateAddToComplexRequest]:
    requests: List[CreateAddToComplexRequest] = []

    for i, (floor_id, riser_id) in enumerate(free_places):
        requests.append(
            CreateAddToComplexRequest(
                apartment_id=apartments[i].id,
                floor_id=floor_id,
                riser_id=riser_id,
            )
        )

    return requests


async def create_apartments(
    container: AsyncContainer,
    users: Sequence[User],
    floors: Sequence[Floor],
) -> Sequence[Apartment]:
    riser_service = await container.get(RiserService)
    risers = await riser_service.list(load=[orm.joinedload(Riser.section)])

    (linked_apartments_to_create, orphan_apartments_to_create, free_places) = (
        generate_apartments(users, floors, risers)
    )

    apartments_service = await container.get(ApartmentService)

    linked_apartments = await apartments_service.create_many(
        linked_apartments_to_create
    )
    orphan_apartments = await apartments_service.create_many(
        orphan_apartments_to_create
    )

    requests_to_create = generate_requests(orphan_apartments, free_places)
    requests_service = await container.get(AddToComplexRequestService)
    await requests_service.create_many(requests_to_create)

    gallery_to_create = generate_gallery([*linked_apartments, *orphan_apartments])
    gallery_service = await container.get(ApartmentGalleryService)
    await gallery_service.create_many(gallery_to_create)

    return linked_apartments
