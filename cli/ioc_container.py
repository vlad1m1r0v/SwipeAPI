from dishka import make_async_container

from config import Config, config

from src.core.ioc import ConfigProvider, SessionProvider
from src.user.ioc import UsersProvider
from src.admin.ioc import AdminProvider
from src.builder.ioc import BuilderProvider
from src.buildings.ioc import BuildingsProvider
from src.apartments.ioc import ApartmentsProvider
from src.announcements.ioc import AnnouncementsProvider
from src.notaries.ioc import NotaryProvider
from src.requests.ioc import RequestsProvider

container = make_async_container(
    ConfigProvider(),
    SessionProvider(),
    UsersProvider(),
    AdminProvider(),
    BuilderProvider(),
    BuildingsProvider(),
    ApartmentsProvider(),
    AnnouncementsProvider(),
    NotaryProvider(),
    RequestsProvider(),
    context={Config: config},
)
