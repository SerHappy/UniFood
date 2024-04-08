from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UsersOrm(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(VARCHAR(255))
    password: Mapped[str] = mapped_column(VARCHAR(255))
    is_verified: Mapped[bool] = mapped_column(default=False)
