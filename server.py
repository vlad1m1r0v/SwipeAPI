from fastapi import FastAPI

from src.core.setup.server import setup

server = FastAPI()

setup(server)
