from pydantic import BaseModel, Field, SecretStr, EmailStr


class EmailConfig(BaseModel):
    host: str = Field(alias="EMAIL_HOST")
    port: int = Field(alias="EMAIL_PORT")
    host_user: EmailStr = Field(alias="EMAIL_HOST_USER")
    host_password: SecretStr = Field(alias="EMAIL_HOST_PASSWORD")
