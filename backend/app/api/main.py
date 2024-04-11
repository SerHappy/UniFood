from app.api.routers import auth, carts, products, registration
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(
    registration.router, prefix="/registration", tags=["registration"]
)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(carts.router, prefix="/cart", tags=["cart"])
