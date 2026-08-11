from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config.settings import get_settings

settings = get_settings()


engine = create_async_engine(
    url=settings.database_url, 
    echo=str(settings.IS_DEBUG).lower() in ("true", "1", "yes"),
    future=True
)

session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

class Base(DeclarativeBase): ...

async def get_session_db() -> AsyncGenerator[AsyncSession,None]:
    """_summary_

    Returns:
        AsyncGenerator[AsyncSession,None]: _description_
    """
    async with session_maker() as session:
        yield session
