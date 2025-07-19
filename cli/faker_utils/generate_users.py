from typing import List, cast


from pydantic import EmailStr

from .faker_instance import fake

from .media_utils import save_file_from_dataset

from src.user.schemas import CreateUserSchema

AMOUNT_OF_USERS = 20
PASSWORD = "Qwerty123#"


def generate_users() -> List[CreateUserSchema]:
    users: List[CreateUserSchema] = []
    for _ in range(AMOUNT_OF_USERS):
        name = fake.name()
        email = fake.custom_email(name)
        photo = save_file_from_dataset(fake.avatar_path())
        phone = fake.ukrainian_phone()
        users.append(
            CreateUserSchema(
                name=name,
                email=cast(EmailStr, email),
                password=PASSWORD,
                photo=photo,
                phone=phone,
            )
        )
    return users
