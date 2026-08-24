from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.router import router as router_auth
from src.tasks.router import router as router_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App start")
    yield
    print("App stop")

app = FastAPI(
    title="Tasks Manager",
    description="Модульный монолит с авторизацией и аутентификацией.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router_auth)
app.include_router(router_task)
