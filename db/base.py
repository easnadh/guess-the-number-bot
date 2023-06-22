from sqlalchemy import URL
from sqlalchemy.ext.declarative import declarative_base

from config import load_config
from db.engine import get_async_engine, get_async_sessionmaker

config = load_config()

postgres_url = URL.create(
    'postgresql+asyncpg',
    database=config.db.database,
    username=config.db.user,
    password=config.db.password,
    host=config.db.host,
    port=config.db.port,
)

async_engine = get_async_engine(postgres_url)
session_maker = get_async_sessionmaker(async_engine)

Base = declarative_base()
