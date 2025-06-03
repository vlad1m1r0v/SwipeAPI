from typing import AsyncIterator, Iterator

import dishka as di

from sqlalchemy.ext import asyncio as sa
from sqlalchemy.orm import Session

from src.users.services import (
    UserService,
    ContactService,
    AgentContactService,
    SubscriptionService,
    NotificationSettingsService,
    BalanceService,
    MonthlyWithdrawalService,
)


class UsersProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_user_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[UserService]:
        async with UserService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_contact_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[ContactService]:
        async with ContactService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_agent_contact_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[AgentContactService]:
        async with AgentContactService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_subscription_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[SubscriptionService]:
        async with SubscriptionService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_notification_settings_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[NotificationSettingsService]:
        async with NotificationSettingsService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_balance_service(
        self,
        session: sa.AsyncSession,
    ) -> AsyncIterator[BalanceService]:
        async with BalanceService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    def provide_monthly_withdrawal_service(
        self, session: Session
    ) -> Iterator[MonthlyWithdrawalService]:
        yield MonthlyWithdrawalService(session=session)
