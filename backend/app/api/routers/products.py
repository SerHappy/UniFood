from app.api.deps import CurrentUser, SessionDep
from app.models import CategoriesOrm, CategoriesProductsOrm, ProductsOrm
from app.schemas.items import CategoryModel, ProductModel
from fastapi import APIRouter, HTTPException
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


@router.get("/product/{product_id}", response_model=ProductModel)
async def get_product(
    session: SessionDep, current_user: CurrentUser, product_id: int
) -> ProductModel | None:
    query = select(ProductsOrm).filter_by(id=product_id)
    product = (await session.execute(query)).scalars().one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
