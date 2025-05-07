from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from src.auth.handlers import auth_router
from src.core.config import Config

from src.auth.ioc import AuthProvider
from src.users.ioc import UserProvider
from src.core.ioc import CoreProvider

load_dotenv()
config: Config = Config()
app = FastAPI()
router = APIRouter()

container = make_async_container(
    AuthProvider(),
    UserProvider(),
    CoreProvider(),
    context={Config: config})

setup_dishka(container=container, app=app)

app.include_router(auth_router)
