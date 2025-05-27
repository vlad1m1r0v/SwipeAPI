import uvicorn

from fastapi import FastAPI

from src.core.setup import setup

server = FastAPI()

setup(server)

if __name__ == "__main__":
    uvicorn.run("server:server", reload=True)
