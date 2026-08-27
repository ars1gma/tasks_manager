from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.engine = engine

    yield 

    engine.dispose()
