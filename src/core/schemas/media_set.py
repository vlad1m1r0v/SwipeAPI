import enum
import re
from typing import Optional

from config import config

from pydantic import BaseModel, Field, model_validator, computed_field


class Action(str, enum.Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


BASE64_URL_REGEX = re.compile(
    r"^data:image/[a-zA-Z0-9.+-]+;base64,[A-Za-z0-9+/]+={0,2}$"
)


class GetGalleryImageSchema(BaseModel):
    id: int
    photo: str = Field(exclude=True)

    @computed_field
    @property
    def photo_url(self) -> Optional[str]:
        return f"{config.server.url}/{self.photo}" if self.photo else None


class Base64Item(BaseModel):
    action: Action
    id: Optional[int] = None
    base64: Optional[str] = Field(
        examples=[
            "data:image/webp;base64,UklGRsYBAABXRUJQVlA4ILoBAAAQBwCdASoZABkAPlEkj0WjoiEUBAA4BQSxgE6ZcQwMtSrgDId+zdj09sCsqOL727JpXxkUk+fXSI8XTKRcmPOoAAD+9WPEOt/QRkR0Fx/6jYW3Ph2WvqZb/WNSAy5f5bTlVdONzxFXAu39tFlQLHk2O22XpgsgRtmCKASeHVHf6VUjUXkqH9pBp3uZlomESkDt2YAwj3EmJGufzx1FNKtdEjvZ1ChhmZs9Avd3PNJNwvHz9Pw986RmTZ750TTyjUn0gQHEYzAK63blnz4pP3M6Rw9zbXm1BVKHYpBWwpGb4vviA90o8iScc+6/xB6i1BBt/Jh5H+KUdoP+Oa+9duR/9WuCz9LOYfce8PPvbctf/ZyCbESy1YIMqYf9SuSbkw/ao3lpwfUfUArZvSf/lzqn6d473t+UNiOXh1V2fvlQK+lOBMEX4qT/6F2I/f/SEK9n4N9uKxZeCg6VXd3kUNI4uGwIEnDw55eLX4BVSmfTxVPPk5uKBJpmPhqeYcILa+fZ8nHTDr7YrojLSTLumbimf2Xkk5+XrJ7wWB+z5xtYel8f/zYxdusDu9K/uf+Lhh6P7lv5O/1jCAAA",
            "data:image/webp;base64,UklGRsIBAABXRUJQVlA4ILYBAABQBwCdASoZABkAPlEkj0WjoiEUBAA4BQSygFOaVTIzW3dwCc670t7A4asDxTkcnZHaX1L1m7Jdt5AoIYT4dbll5dgAAP7in8HZC5zZsdHtPgGcEunqftrMqMEG7xqFUlSBV9khTxkKvSPGQyDAL1zb2+Y4Xe15EMrz1achYZQe7KbogdXsff/pMO/rpoiXl0BFt+4MCDDtOyVvqCRvZ/HGJ97FzntWctO123H/8uaDOX7A5yvuuR2FE2FLUN/aVNLXQ2qNEn/FLBBE2+Hu+NsuM6ckpypPI6mcFndYYDMi78vxeJEkd0nuA7hk0R8mALb/7+fgb2HkoIwQm7BZ0yBwNG1wVDLA/IXBsW8hIIo3KcwLPJMy09G67X5Qi4A7RPez2XkOyyPOHLcZNx2sNRNXfU1S4k5W3aFk58XW7T7cwpt1lYVDfNqytULfWzkYdPfsVgsJXk2qINvZSwIojIGmdPlK5VwJZz60JfsR+X4G7QFHmWrXXFbw/vV9tP8B0/3UrWzXaLQAecuj1CLNTgFOxdEV/z9gh7ehoaE8vj/+Kt8aDRP+MAz2f5hoOuVw/z//0G/AAAA=",
            "data:image/webp;base64,UklGRnwDAABXRUJQVlA4WAoAAAAgAAAAGAAAGAAASUNDUOABAAAAAAHgbGNtcwQgAABtbnRyUkdCIFhZWiAH4gADABQACQAOAB1hY3NwTVNGVAAAAABzYXdzY3RybAAAAAAAAAAAAAAAAAAA9tYAAQAAAADTLWhhbmR56b9WWj4BtoMjhVVG90+qAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAApkZXNjAAAA/AAAACRjcHJ0AAABIAAAACJ3dHB0AAABRAAAABRjaGFkAAABWAAAACxyWFlaAAABhAAAABRnWFlaAAABmAAAABRiWFlaAAABrAAAABRyVFJDAAABwAAAACBnVFJDAAABwAAAACBiVFJDAAABwAAAACBtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAYAAAAcAEMAQwAwAABYWVogAAAAAAAA9tYAAQAAAADTLXNmMzIAAAAAAAEMPwAABd3///MmAAAHkAAA/ZL///uh///9ogAAA9wAAMBxWFlaIAAAAAAAAG+gAAA48gAAA49YWVogAAAAAAAAYpYAALeJAAAY2lhZWiAAAAAAAAAkoAAAD4UAALbEcGFyYQAAAAAAAwAAAAJmaQAA8qcAAA1ZAAAT0AAACltWUDggdgEAAJAGAJ0BKhkAGQA+USSPRaOiIRQEADgFBLGAWdCCcYBugxcHOMN6p05RwChWhilgMYUm6OGRyBbRJ1+Ew3gA/v7Yo4WpgCU7zwXRJq87pl0B5xSe01V+2YpKU6rBuon9Prr32h9/dlGMxTl4xSeoGy8NmYws3IZfmd9CiT09TDyu/eXKnUE/TvNh/gmD5vMctdZHfNfzpqEoS45CMmgo8R3BkGF7bBdy4QfyJ9VuRf/gAj9NI/VfXt7iK1nGChVQKPtEIhL4giA9T5oLsQN/8ID7f7KXjkkypD0/OHtHHM07r6QTH8b/TqDxYOj9JVwmcGOuhKOsTnj0+kqpVxdFO3nizPAl2QnHNLeeA1Zu6P4Iun78YEPRXHXqZ3SfKw2sBJkaHaNN7Mr3cE5uoowxHCOcZLb/3mNv9UjvlXpoWd/Xd1tmtaBeh+EpXJiPb6p/pHbq/erQYUFfI/3SrvpWV4C7tWhJ/kg+hxIdnsuxJ0Mk9JyONwAA",
        ],
        default=None,
    )
    order: Optional[int] = None

    @model_validator(mode="after")
    def validate_all(self) -> "Base64Item":
        if self.action == Action.CREATED and self.id is not None:
            raise ValueError("Newly created item cannot have an ID.")

        if self.action in {Action.UPDATED, Action.DELETED} and self.id is None:
            raise ValueError(f"{self.action.value.title()} item must have an ID.")

        if self.action == Action.CREATED:
            if not self.base64:
                raise ValueError("Base64 image required for newly created item.")
            if not BASE64_URL_REGEX.fullmatch(self.base64):
                raise ValueError("Invalid base64 format.")
        else:
            if self.base64:
                raise ValueError("Base64 image should only be sent for created items.")

        if self.action == Action.DELETED and self.order is not None:
            raise ValueError("Deleted item cannot have order set.")

        return self
