from collections.abc import Generator
from typing import Annotated

from app.core import security
from app.core.config import settings
from app.core.db import Session
from app.models.users import UsersOrm
from app.schemas.tokens import AccessTokenPayload
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)


async def get_db() -> Generator[AsyncSession, None, None]:  # type: ignore
    async with Session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(session: SessionDep, token: TokenDep) -> UsersOrm:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM],
        )
        token_data = AccessTokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=403, detail=f"Could not validate credentials {e}"
        )
    user = await session.get(UsersOrm, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Not verified")
    return user


CurrentUser = Annotated[UsersOrm, Depends(get_current_user)]
