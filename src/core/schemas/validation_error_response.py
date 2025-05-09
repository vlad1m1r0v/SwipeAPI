from typing import Dict

from pydantic import Field, BaseModel


class ValidationErrorResponse(BaseModel):
    detail: Dict[str, str] = Field(
        examples=[
            {
                "errors": {
                    "field": "field does not match certain criteria",
                }
            }
        ]
    )
