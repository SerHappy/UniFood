from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import settings
from app.core.db import Session
from app.models.users import UsersOrm
from app.schemas.tokens import AccessTokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)
optional_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token",
    auto_error=False,
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]
OptionalTokenDep = Annotated[str | None, Depends(optional_oauth2)]


async def get_db() -> AsyncGenerator[None, None]:
    """
    Получает сессию базы данных для выполнения запросов.

    Это асинхронный контекстный менеджер, который открывает сессию,
    предоставляет её в качестве генератора, и закрывает после завершения операций.

    :return: Экземпляр сессии SQLAlchemy для асинхронного использования
    :rtype: AsyncGenerator[None, None]
    """
    async with Session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(session: SessionDep, token: TokenDep) -> UsersOrm:
    """Зависимость для получения текущего пользователя.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param token: Зависимость для получения токена.
    :type token: TokenDep
    :raises invalid_credentials: Ошибка получения пользователя.
    :return: Объект SQLAlchemy модели пользователя.
    :rtype: UsersOrm
    """
    invalid_credentials = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM],
        )
        token_data = AccessTokenPayload(**payload)
    except (JWTError, ValidationError):
        raise invalid_credentials
    user = await session.get(UsersOrm, token_data.sub)
    if not user:
        raise invalid_credentials
    if not user.is_verified:
        raise invalid_credentials
    return user


CurrentUser = Annotated[UsersOrm, Depends(get_current_user)]


async def get_optional_current_user(
    session: SessionDep,
    token: OptionalTokenDep,
) -> UsersOrm | None:
    """Зависимость для получения текущего пользователя (опционально).

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param token: Зависимость для получения токена доступа если он есть.
    :type token: OptionalTokenDep
    :return: Объект SQLAlchemy модели пользователя если он существует.
    :rtype: UsersOrm | None
    """
    if not token:
        return None
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = AccessTokenPayload(**payload)
        user = await session.get(UsersOrm, token_data.sub)
        if user and user.is_verified:
            return user
    except (JWTError, ValidationError):
        return None
    return None


CurrentOptionalUser = Annotated[UsersOrm | None, Depends(get_optional_current_user)]
