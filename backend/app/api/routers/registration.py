from fastapi import APIRouter, BackgroundTasks
from fastapi.exceptions import HTTPException

from app.api.deps import SessionDep
from app.db import crud
from app.schemas.messages import Message
from app.schemas.users import UserCreate, UserPublic, UserRegister
from app.services.mail import (
    generate_confirmation_email,
    generate_confirmation_token,
    send_email,
    verify_confirmation_token,
)

router = APIRouter()


@router.post("/", response_model=UserPublic)
async def create_user(
    session: SessionDep,
    user_in: UserRegister,
    background_tasks: BackgroundTasks,
) -> UserPublic:
    """Эндпоинт для регистрации пользователя.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param user_in: Схема данных для регистрации пользователя.
    :type user_in: UserRegister
    :param background_tasks: Объект для добавления задач в очередь.
    :type background_tasks: BackgroundTasks
    :raises HTTPException: Ошибки при регистрации пользователя.
    :return: Схема Pydantic с информацией о пользователе.
    :rtype: UserPublic
    """
    user = await crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_create = UserCreate(**user_in.model_dump())
    user_orm = await crud.create_user(session=session, user=user_create)
    html = generate_confirmation_email(generate_confirmation_token(user_orm.email))
    background_tasks.add_task(
        send_email,
        user_orm.email,
        "Подтвердите электронную почту",
        html,
    )
    return UserPublic.model_validate(user_orm)


@router.get("/confirm")
async def confirm_email(session: SessionDep, token: str) -> Message:
    """Эндпоинт для подтверждения почты.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param token: Токен для подтверждения почты.
    :type token: str
    :raises HTTPException: Ошибки при подтверждении почты.
    :return: Схема Pydantic с сообщением о подтверждении почты.
    :rtype: Message
    """
    email = verify_confirmation_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await crud.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")
    await crud.verify_user(session=session, user=user)
    return Message(message="Почта подтверждена")
