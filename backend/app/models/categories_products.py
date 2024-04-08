from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CategoriesProductsOrm(Base):
    __tablename__ = "categories_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
