from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep
from app.core import security
from app.core.config import settings
from app.db import crud
from app.schemas.tokens import AccessToken

router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AccessToken:
    """Эндпоинт для генерации токена доступа.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param form_data: Зависимость для получения данных формы. Хранит в себе username и password.
    :type form_data: Annotated[OAuth2PasswordRequestForm, Depends]
    :raises HTTPException: Ошибка авторизации.
    :return: Схему Pydantic с токеном доступа.
    :rtype: AccessToken
    """
    user = await crud.authenticate(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Not verified")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return AccessToken(
        access_token=security.create_access_token(
            {"sub": str(user.id)}, access_token_expires
        )
    )
