from pydantic import BaseModel


class UserCart(BaseModel):
    id: int
    items: list["CartItem"]
    total: int
    discount: int
    to_pay: int


class CartItem(BaseModel):
    product_id: int
    name: str
    price_per_one: int
    weight: int
    photo_url: str
    full_price: int
    quantity: int


class CartItemAdd(BaseModel):
    product_id: int


class CartItemRemove(BaseModel):
    product_id: int
