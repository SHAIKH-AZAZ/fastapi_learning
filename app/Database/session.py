from fastapi import Depends
from typing_extensions import Annotated
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.config import settings

engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True,
)

from .models import Shipment


async def create_db_tables():
    async with engine.begin() as connection:
        from app.api.schema import shipment
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    Async_Session   =async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with Async_Session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
