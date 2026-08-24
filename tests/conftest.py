import asyncio
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.config.database import Base, get_session_db
from src.config.settings import get_settings
from src.main import app

settings = get_settings()

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
test_async_sessionmaker = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture(scope="session")
async def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def prepare_database():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session():
    async with test_engine.connect() as connection:
        transaction = await connection.begin()

        async with test_async_sessionmaker(bind=connection) as session:
            yield session

        await transaction.rollback()

@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    def _override_get_db():
        return db_session

    app.dependency_overrides[get_session_db] = _override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="https://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def anyio_backend():
    """Переопределяем фикстуру anyio на уровень session, чтобы убрать ScopeMismatch."""
    return "asyncio"
