from typing import Optional

from fastapi import (
    Form,
    UploadFile,
    File
)

from src.users.schemas import UpdateUserSchema


def update_user_form(
        name: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        photo: Optional[UploadFile] = File(None),
) -> tuple[UpdateUserSchema, Optional[UploadFile]]:
    data = UpdateUserSchema(name=name, email=email, phone=phone)
    return data, photo


__all__ = ["update_user_form"]
