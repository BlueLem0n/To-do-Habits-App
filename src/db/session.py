from fastapi import Depends
from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from core.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=settings.DB_ECHO)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]