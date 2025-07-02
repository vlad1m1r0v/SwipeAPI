# -*- coding: utf-8 -*-
"""
Examples generator module.
"""

from typing import Type

from starlette import status

from src.auth.exceptions import (
    TokenNotProvidedException,
    InvalidTokenTypeException,
    InvalidTokenException,
    UnauthorizedException,
)

from src.user.exceptions import (
    SubscriptionExpiredException,
    UserBlacklistedException,
    InvalidRoleException,
)

from src.core.utils.errors.base import DefaultHTTPException


class ExamplesGenerator:
    """
    Class to generate the examples for the OpenAPI docs.
    """

    auth_error = (
        TokenNotProvidedException,
        InvalidTokenTypeException,
        InvalidTokenException,
        UnauthorizedException,
        InvalidRoleException,
    )

    user_auth_error = (UserBlacklistedException, SubscriptionExpiredException)

    @staticmethod
    def generate_nested_schema_for_code(responses, error_code):
        """
        Generate the nested schema for the given error code.
        """
        responses[error_code] = {}
        responses[error_code]["content"] = {}
        responses[error_code]["content"]["application/json"] = {}

    @classmethod
    def generate_examples(
        cls,
        *args: Type[DefaultHTTPException],
        auth: bool = False,
        is_user: bool = False,
    ) -> dict:
        """
        Generate the error responses for the OpenAPI docs.
        """
        responses: dict = {}
        if auth:
            args += cls.auth_error

        if is_user:
            args += cls.user_auth_error

        error_codes = {error.status_code for error in args}

        for error_code in error_codes:
            examples = {}

            for error in args:
                instance = error()  # noqa
                if instance.status_code == error_code:
                    examples[instance.error] = instance.example()

            cls.generate_nested_schema_for_code(responses, error_code)
            responses[error_code]["content"]["application/json"]["examples"] = examples

        cls.change_422_validation_schema(responses)

        return responses

    @classmethod
    def change_422_validation_schema(cls, responses):
        """
        Change the 422 validation schema to match the one used in the.

        API.

        """
        cls.generate_nested_schema_for_code(
            responses, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        example = {
            "validation_errors": {
                "summary": "Validation Error",
                "value": {
                    "status": 422,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "details": [
                            {
                                "location": "string",
                                "field": "string",
                                "message": "string",
                            },
                        ],
                    },
                },
            },
        }
        responses[status.HTTP_422_UNPROCESSABLE_ENTITY]["content"]["application/json"][
            "examples"
        ] = example


generate_examples = ExamplesGenerator.generate_examples
