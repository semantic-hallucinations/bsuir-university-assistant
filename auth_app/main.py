from .database import init_db, close_db_connections

from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app: FastAPI):
    await init_db()
    yield
    await close_db_connections()

version = "v1"

auth_app = FastAPI(lifespan=life_span)

@auth_app.get("/")
async def root():
    return {"message": "youre in root"}


