from app.core.security import get_password_hash, verify_password
from app.models import UsersOrm
from app.schemas.users import UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_email(session: AsyncSession, email: str) -> UsersOrm | None:
    stmt = select(UsersOrm).filter_by(email=email)
    session_user = (await session.execute(stmt)).scalars().first()
    return session_user


async def create_user(session: AsyncSession, user: UserCreate) -> UsersOrm:
    hashed_password = get_password_hash(user.password)
    user_orm = UsersOrm(**user.model_dump())
    user_orm.password = hashed_password
    session.add(user_orm)
    await session.commit()
    await session.refresh(user_orm)
    return user_orm


async def verify_user(session: AsyncSession, user: UsersOrm) -> UsersOrm | None:
    user.is_verified = True
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate(
    session: AsyncSession, email: str, password: str
) -> UsersOrm | None:
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
