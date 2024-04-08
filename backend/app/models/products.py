from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ProductsOrm(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    price: Mapped[float]
    composition: Mapped[str | None]
    description: Mapped[str | None]
    weight: Mapped[int | None]
    photo_url: Mapped[str] = mapped_column(VARCHAR(255))
    rating: Mapped[float | None]
    is_in_stock: Mapped[bool] = mapped_column(default=True)
