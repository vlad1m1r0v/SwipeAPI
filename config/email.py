from pydantic import (
    BaseModel,
    Field,
    SecretStr,
    EmailStr
)


class EmailConfig(BaseModel):
    email_host: str = Field(alias='EMAIL_HOST')
    email_port: int = Field(alias='EMAIL_PORT')
    email_host_user: EmailStr = Field(alias='EMAIL_HOST_USER')
    email_host_password: SecretStr = Field(alias='EMAIL_HOST_PASSWORD')