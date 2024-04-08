from collections.abc import Generator
from typing import Annotated

from app.core.db import Session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> Generator[AsyncSession, None, None]:  # type: ignore
    async with Session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
