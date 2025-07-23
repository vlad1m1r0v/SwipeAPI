import random

from typing import Sequence, List

from datetime import time, datetime, timedelta

from dishka import AsyncContainer

from .faker_instance import fake

from src.announcements.enums import Colour, Phrase
from src.announcements.models import Announcement
from src.announcements.schemas import (
    CreateAnnouncementSchema,
    CreatePromotionSchema,
    CreateViewSchema,
    CreateFavouriteAnnouncementSchema,
    CreateFilterSchema,
)
from src.announcements.services import (
    AnnouncementService,
    AnnouncementPromotionService,
    AnnouncementViewService,
    AnnouncementFavouriteService,
    AnnouncementFilterService,
)

from src.builder.enums import (
    Type,
    Status,
    PropertyType,
    BillingOptions,
)

from src.apartments.enums import Rooms, Finishing
from src.apartments.models import Apartment

from src.user.models import User


def generate_announcements(
    apartments: Sequence[Apartment],
) -> List[CreateAnnouncementSchema]:
    announcements: List[CreateAnnouncementSchema] = []

    for apartment in apartments:
        announcements.append(
            CreateAnnouncementSchema(
                apartment_id=apartment.id,
                is_relevant=True,
                viewing_time=fake.custom_time(time(8, 0), time(21, 0)),
            )
        )

    return announcements


def generate_promotions(
    announcements: Sequence[Announcement],
) -> List[CreatePromotionSchema]:
    promotions: List[CreatePromotionSchema] = []

    now = datetime.now()

    for announcement in announcements:
        promotions.append(
            CreatePromotionSchema(
                announcement_id=announcement.id,
                highlight_colour=fake.enum(Colour),
                highlight_expiry_date=fake.date_time_between_dates(
                    now + timedelta(days=30), now + timedelta(days=90)
                ),
                phrase=fake.enum(Phrase),
                phrase_expiry_date=fake.date_time_between_dates(
                    now + timedelta(days=30), now + timedelta(days=90)
                ),
                big_advert_expiry_date=fake.date_time_between_dates(
                    now + timedelta(days=30), now + timedelta(days=90)
                ),
                boost_expiry_date=fake.date_time_between_dates(
                    now + timedelta(days=30), now + timedelta(days=90)
                ),
            )
        )

    return promotions


def generate_views(
    announcements: Sequence[Announcement], users: Sequence[User]
) -> List[CreateViewSchema]:
    views: List[CreateViewSchema] = []

    for user in users:
        for _ in range(fake.pyint(min_value=10, max_value=30)):
            views.append(
                CreateViewSchema(
                    user_id=user.id,
                    announcement_id=fake.random_element(announcements).id,
                )
            )

    return views


def generate_favourite_announcements(
    announcements: Sequence[Announcement], users: Sequence[User]
) -> List[CreateFavouriteAnnouncementSchema]:
    favourites: List[CreateFavouriteAnnouncementSchema] = []

    for user in users:
        amount = fake.pyint(min_value=10, max_value=30)
        picked_announcements: List[Announcement] = random.sample(announcements, amount)

        for picked_announcement in picked_announcements:
            favourites.append(
                CreateFavouriteAnnouncementSchema(
                    user_id=user.id,
                    announcement_id=picked_announcement.id,
                )
            )

    return favourites


def generate_filters(users: Sequence[User]) -> List[CreateFilterSchema]:
    filters: List[CreateFilterSchema] = []

    for user in users:
        for _ in range(fake.pyint(min_value=2, max_value=5)):
            filter_to_create = {
                "type": fake.enum(Type),
                "status": fake.enum(Status),
                "district": fake.city(),
                "neighbourhood": fake.street_name(),
                "rooms": fake.enum(Rooms),
                "price_min": fake.random_int(min=30000, max=35000),
                "price_max": fake.random_int(min=70000, max=200000),
                "area_min": fake.pydecimal(min_value=30, max_value=40, right_digits=1),
                "area_max": fake.pydecimal(min_value=60, max_value=150, right_digits=1),
                "property_type": fake.enum(PropertyType),
                "billing_options": fake.enum(BillingOptions),
                "finishing": fake.enum(Finishing),
            }

            keys = list(filter_to_create.keys())
            num_to_remove = len(keys) // 2
            keys_to_remove = random.sample(keys, k=num_to_remove)

            for key in keys_to_remove:
                del filter_to_create[key]

            filters.append(
                CreateFilterSchema(
                    user_id=user.id,
                    **filter_to_create,
                )
            )

    return filters


async def create_announcements(
    container: AsyncContainer, apartments: Sequence[Apartment], users: Sequence[User]
) -> None:
    announcements_to_create = generate_announcements(apartments)
    announcement_service = await container.get(AnnouncementService)
    announcements = await announcement_service.create_many(announcements_to_create)

    promotions_to_create = generate_promotions(announcements)
    promotion_service = await container.get(AnnouncementPromotionService)
    await promotion_service.create_many(promotions_to_create)

    views_to_create = generate_views(announcements, users)
    view_service = await container.get(AnnouncementViewService)
    await view_service.create_many(views_to_create)

    favourites_to_create = generate_favourite_announcements(announcements, users)
    favourite_service = await container.get(AnnouncementFavouriteService)
    await favourite_service.create_many(favourites_to_create)

    filters_to_create = generate_filters(users)
    filter_service = await container.get(AnnouncementFilterService)
    await filter_service.create_many(filters_to_create)
