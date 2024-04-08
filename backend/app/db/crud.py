from app.core.security import get_password_hash
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
