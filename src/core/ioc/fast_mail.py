import dishka as di

from fastapi_mail import (
    FastMail,
    ConnectionConfig
)

from config import Config


class FastMailProvider(di.Provider):
    @di.provide(scope=di.Scope.APP)
    def provide_fast_mail(self, config: Config) -> FastMail:
        conf = ConnectionConfig(
            MAIL_USERNAME=str(config.email.email_host_user),
            MAIL_PASSWORD=config.email.email_host_password,
            MAIL_FROM=config.email.email_host_user,
            MAIL_PORT=config.email.email_port,
            MAIL_SERVER=config.email.email_host,
            MAIL_FROM_NAME="Swipe",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )

        fast_mail = FastMail(conf)
        return fast_mail