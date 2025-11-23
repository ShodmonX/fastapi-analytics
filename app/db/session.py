from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from .base import LocalSession


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with LocalSession() as session:
        yield session