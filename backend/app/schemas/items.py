from pydantic import BaseModel


class CategoryModel(BaseModel):
    id: int
    name: str
    products: list["ProductModel"] = []


from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int
    name: str
    price: int
    weight: int | None = None
    photo_url: str
    rating: float | None = None

