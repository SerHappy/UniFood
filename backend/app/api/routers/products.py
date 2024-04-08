from app.api.deps import SessionDep
from app.models import CategoriesOrm, CategoriesProductsOrm, ProductsOrm
from app.schemas.items import CategoryModel, ProductModel
from fastapi import APIRouter
from sqlalchemy import select

router = APIRouter()


@router.get("/all/", response_model=list[CategoryModel])
async def read_categories_with_products(session: SessionDep) -> list[CategoryModel]:
    query = select(CategoriesOrm)
    categories: list[CategoriesOrm] = (await session.execute(query)).scalars().all()
    categories_with_products = []
    for category in categories:
        query = (
            select(ProductsOrm)
            .join(
                CategoriesProductsOrm,
                ProductsOrm.id == CategoriesProductsOrm.product_id,
            )
            .filter_by(category_id=category.id)
        )
        products: list[ProductsOrm] = (await session.execute(query)).scalars().all()
        category_data = CategoryModel(
            id=category.id,
            name=category.name,
            products=[ProductModel(**product.__dict__) for product in products],
        )
        categories_with_products.append(category_data)
    return categories_with_products
