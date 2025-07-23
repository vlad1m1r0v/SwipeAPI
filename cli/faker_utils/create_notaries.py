from typing import List, cast

from dishka import AsyncContainer

from pydantic import EmailStr

from src.admin.services import NotaryService
from src.admin.schemas import CreateNotarySchema

from .faker_instance import fake
from .media_utils import save_file_from_dataset
from .contstants import NOTARIES_TOTAL


def generate_notaries() -> List[CreateNotarySchema]:
    notaries: List[CreateNotarySchema] = []

    for _ in range(NOTARIES_TOTAL):
        first_name: str = fake.first_name()
        last_name: str = fake.last_name()
        photo = save_file_from_dataset(fake.avatar_path())
        phone = fake.ukrainian_phone()
        email = fake.custom_user_email(f"{first_name} {last_name}")

        notaries.append(
            CreateNotarySchema(
                first_name=first_name,
                last_name=last_name,
                email=cast(EmailStr, email),
                photo=photo,
                phone=phone,
            )
        )

    return notaries


async def create_notaries(container: AsyncContainer) -> None:
    notaries_to_create = generate_notaries()
    notary_service = await container.get(NotaryService)
    await notary_service.create_many(notaries_to_create)
