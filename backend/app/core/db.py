from app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=settings.SQLALCHEMY_ECHO,
)
Session: async_sessionmaker = async_sessionmaker(engine)
