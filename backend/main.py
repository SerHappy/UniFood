import asyncpg
from decouple import config
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int
    name: str
    price: int
    weight: int | None = None
    photo_url: str
    rating: float | None = None


class CategoryModel(BaseModel):
    id: int
    name: str
    products: list[ProductModel] = []


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_db():
    pool = await asyncpg.create_pool(config("DATABASE_URL"))
    if pool is None:
        raise Exception("Failed to connect to database")
    try:
        yield pool
    finally:
        await pool.close()


@app.get("/categories/products/", response_model=list[CategoryModel])
async def read_categories_with_products(db=Depends(get_db)) -> list:
    async with db.acquire() as conn:
        categories = await conn.fetch("SELECT * FROM categories")
        categories_with_products = []
        for category in categories:
            products = await conn.fetch(
                """
                SELECT p.id, p.name, p.price, p.weight, p.photo_url, COALESCE(p.rating, 0.0) as rating FROM products p
                JOIN product_categories pc ON p.id = pc.product_id
                WHERE pc.category_id = $1
            """,
                category["id"],
            )
            category_data = CategoryModel(
                id=category["id"],
                name=category["name"],
                products=[ProductModel(**product) for product in products],
            )
            categories_with_products.append(category_data)
        return categories_with_products
