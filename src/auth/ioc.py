from typing import Iterator

from config import Config

import dishka as di

from redis.asyncio import Redis

from src.auth.services import AuthService, SignService, JwtService

from src.users.services import (
    UserService,
    ContactService,
    AgentContactService,
    SubscriptionService,
    NotificationSettingsService,
    BalanceService,
)

from src.admins.services import BlacklistService

from src.builders.services import (
    ComplexService,
    InfrastructureService,
    AdvantagesService,
    FormalizationAndPaymentSettingsService,
)


class AuthProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    def provide_jwt_service(
        self,
        config: Config,
    ) -> Iterator[JwtService]:
        yield JwtService(config=config)

    @di.provide(scope=di.Scope.REQUEST)
    def provide_sign_service(
        self,
        config: Config,
        redis: Redis,
    ) -> Iterator[SignService]:
        yield SignService(config=config, redis=redis)

    @di.provide(scope=di.Scope.REQUEST)
    def provide_auth_service(
        self,
        jwt_service: JwtService,
        sign_service: SignService,
        user_service: UserService,
        blacklist_service: BlacklistService,
        contact_service: ContactService,
        agent_contact_service: AgentContactService,
        subscription_service: SubscriptionService,
        notification_settings_service: NotificationSettingsService,
        balance_service: BalanceService,
        complex_service: ComplexService,
        infrastructure_service: InfrastructureService,
        advantages_service: AdvantagesService,
        formalization_and_payment_settings_service: FormalizationAndPaymentSettingsService,
    ) -> Iterator[AuthService]:
        yield AuthService(
            jwt_service=jwt_service,
            sign_service=sign_service,
            user_service=user_service,
            blacklist_service=blacklist_service,
            contact_service=contact_service,
            agent_contact_service=agent_contact_service,
            subscription_service=subscription_service,
            notification_settings_service=notification_settings_service,
            balance_service=balance_service,
            complex_service=complex_service,
            infrastructure_service=infrastructure_service,
            advances_service=advantages_service,
            formalization_and_payment_settings_service=formalization_and_payment_settings_service,
        )


__all__ = ["AuthProvider"]
