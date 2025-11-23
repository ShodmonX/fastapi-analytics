from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app import settings


engine = create_async_engine(settings.DATABASE_URL)

LocalSession = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass