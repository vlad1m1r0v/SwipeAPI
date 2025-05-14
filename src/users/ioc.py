from typing import AsyncIterator

import dishka as di
from sqlalchemy.ext import asyncio as sa

from src.users import services as s


class UsersProvider(di.Provider):
    @di.provide(scope=di.Scope.REQUEST)
    async def provide_user_service(
            self,
            session: sa.AsyncSession,
    ) -> AsyncIterator[s.UserService]:
        async with s.UserService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_contact_service(
            self,
            session: sa.AsyncSession,
    ) -> AsyncIterator[s.ContactService]:
        async with s.ContactService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_agent_contact_service(
            self,
            session: sa.AsyncSession,
    ) -> AsyncIterator[s.AgentContactService]:
        async with s.AgentContactService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_subscription_service(
            self,
            session: sa.AsyncSession,
    ) -> AsyncIterator[s.SubscriptionService]:
        async with s.SubscriptionService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_notification_settings_service(
            self,
            session: sa.AsyncSession,
    ) -> AsyncIterator[s.NotificationSettingsService]:
        async with s.NotificationSettingsService.new(session=session) as service:
            yield service

    @di.provide(scope=di.Scope.REQUEST)
    async def provide_balance_service(
            self,
            session: sa.AsyncSession,
    ) -> AsyncIterator[s.BalanceService]:
        async with s.UserService.new(session=session) as service:
            yield service