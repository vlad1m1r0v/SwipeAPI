import os
import random
import re


from faker import Faker
from faker.providers import DynamicProvider, BaseProvider

from src.core.constants import DATASETS_DIR

AVATARS_DIR = DATASETS_DIR / "avatars"
DOCUMENTS_DIR = DATASETS_DIR / "documents"
BUILDINGS_DIR = DATASETS_DIR / "buildings"
ROOMS_DIR = DATASETS_DIR / "rooms"
SCHEMES_DIR = DATASETS_DIR / "schemes"

fake = Faker()

avatar_path_provider = DynamicProvider(
    provider_name="avatar_path",
    elements=[
        os.path.join(AVATARS_DIR, filename) for filename in os.listdir(AVATARS_DIR)
    ],
)

document_path_provider = DynamicProvider(
    provider_name="document_path",
    elements=[
        os.path.join(DOCUMENTS_DIR, filename) for filename in os.listdir(DOCUMENTS_DIR)
    ],
)

building_path_provider = DynamicProvider(
    provider_name="building_path",
    elements=[
        os.path.join(BUILDINGS_DIR, filename) for filename in os.listdir(BUILDINGS_DIR)
    ],
)

room_path_provider = DynamicProvider(
    provider_name="room_path",
    elements=[os.path.join(ROOMS_DIR, filename) for filename in os.listdir(ROOMS_DIR)],
)

scheme_path_provider = DynamicProvider(
    provider_name="scheme_path",
    elements=[
        os.path.join(SCHEMES_DIR, filename) for filename in os.listdir(SCHEMES_DIR)
    ],
)


class UkrainianPhoneProvider(BaseProvider):
    @staticmethod
    def ukrainian_phone() -> str:
        return f"+380{random.randint(400000000, 999999999)}"


class CustomEmailProvider(BaseProvider):
    @staticmethod
    def custom_email(name: str) -> str:
        return f"{re.sub(r'[ .]', '_', name.lower())}_{fake.random_int(min=1950, max=1990)}@gmail.com"


fake.add_provider(avatar_path_provider)
fake.add_provider(document_path_provider)
fake.add_provider(building_path_provider)
fake.add_provider(room_path_provider)
fake.add_provider(scheme_path_provider)
fake.add_provider(UkrainianPhoneProvider)
fake.add_provider(CustomEmailProvider)
