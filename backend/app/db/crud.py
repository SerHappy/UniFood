from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models import UsersOrm
from app.schemas.users import UserCreate


async def get_user_by_email(session: AsyncSession, email: str) -> UsersOrm | None:
    """Получение пользователя по почте из базы данных.

    :param session: Объект сессии базы данных.
    :type session: AsyncSession
    :param email: Электронная почта пользователя.
    :type email: str
    :return: Пользователь или None.
    :rtype: UsersOrm | None
    """
    stmt = select(UsersOrm).filter_by(email=email)
    session_user = (await session.execute(stmt)).scalars().first()
    return session_user


async def create_user(session: AsyncSession, user: UserCreate) -> UsersOrm:
    """Создание пользователя в базе данных.

    :param session: Объект сессии базы данных.
    :type session: AsyncSession
    :param user: Схема данных пользователя.
    :type user: UserCreate
    :return: Пользователь.
    :rtype: UsersOrm
    """
    hashed_password = get_password_hash(user.password)
    user_orm = UsersOrm(**user.model_dump())
    user_orm.password = hashed_password
    session.add(user_orm)
    await session.commit()
    await session.refresh(user_orm)
    return user_orm


async def verify_user(session: AsyncSession, user: UsersOrm) -> UsersOrm | None:
    """Подтверждение почты пользователя в базе данных.

    :param session: Объект сессии базы данных.
    :type session: AsyncSession
    :param user: Пользователь.
    :type user: UsersOrm
    :return: Пользователь.
    :rtype: UsersOrm | None
    """
    user.is_verified = True
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate(
    session: AsyncSession,
    email: str,
    password: str,
) -> UsersOrm | None:
    """Аутентификация пользователя по почте и паролю.

    :param session: Объект сессии базы данных.
    :type session: AsyncSession
    :param email: Электронная почта пользователя.
    :type email: str
    :param password: Пароль пользователя.
    :type password: str
    :return: Пользователь или None.
    :rtype: UsersOrm | None
    """
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
