import uvicorn

from fastapi import FastAPI

from src.core.setup.server import setup

server = FastAPI()

setup(server)

if __name__ == "__main__":
    uvicorn.run("server:server", reload=True)
