from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker


def get_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(url=url)


async def get_models(engine: AsyncEngine, metadata: MetaData) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


def get_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
