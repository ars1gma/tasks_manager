from fastapi import FastAPI

from src.app_lifespan import lifespan
from src.auth.router import router as router_auth
from src.middlewares import LogAndErrorsMiddleware
from src.tasks.router import router as router_task

app = FastAPI(
    title="Tasks Manager",
    description="Модульный монолит с авторизацией и аутентификацией.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router_auth)
app.include_router(router_task)

app.add_middleware(LogAndErrorsMiddleware)