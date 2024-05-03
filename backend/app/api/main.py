from fastapi import APIRouter
from yookassa import Configuration

from app.api.routers import auth, carts, products, registration
from app.core.config import settings

Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(
    registration.router, prefix="/registration", tags=["registration"]
)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(carts.router, prefix="/cart", tags=["cart"])
