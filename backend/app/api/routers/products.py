from app.api.deps import CurrentOptionalUser, CurrentUser, SessionDep
from app.models import CategoriesOrm, CategoriesProductsOrm, ProductsOrm
from app.models.cart_items import CartItemsOrm
from app.schemas.carts import CartItemAdd
from app.schemas.items import CategoryModel, ProductInfo, ProductModel
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

router = APIRouter()


@router.get("/all/", response_model=list[CategoryModel])
async def read_categories_with_products(
    session: SessionDep,
    user: CurrentOptionalUser,
) -> list[CategoryModel]:
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

        if user:
            cart_items_orm: list[CartItemsOrm] = (
                (
                    await session.execute(
                        select(CartItemsOrm)
                        .options(joinedload(CartItemsOrm.product))
                        .where(CartItemsOrm.user_id == user.id)
                    )
                )
                .scalars()
                .all()
            )

            cart_items = {item.product_id: item.quantity for item in cart_items_orm}
        else:
            cart_items = {}

        category_data = CategoryModel(
            id=category.id,
            name=category.name,
            products=[
                ProductModel(**product.__dict__, in_cart=cart_items.get(product.id, 0))
                for product in products
            ],
        )
        categories_with_products.append(category_data)
    return categories_with_products


@router.get("/info/{product_id}", response_model=ProductInfo)
async def product_info(product_id: int, session: SessionDep) -> ProductInfo:
    product = await session.get(ProductsOrm, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductInfo(**product.__dict__)


@router.post("/add")
async def add_item_to_cart(
    session: SessionDep,
    user: CurrentUser,
    item: CartItemAdd,
) -> ProductModel:
    product = await session.get(ProductsOrm, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_in_cart = (
        await session.execute(
            select(CartItemsOrm)
            .options(joinedload(CartItemsOrm.product))
            .where(
                CartItemsOrm.user_id == user.id,
                CartItemsOrm.product_id == item.product_id,
            )
        )
    ).scalar_one_or_none()

    if product_in_cart:
        product_in_cart.quantity += 1
    else:
        product_in_cart = CartItemsOrm(
            user_id=user.id, product_id=item.product_id, quantity=1
        )
        session.add(product_in_cart)

    product = ProductModel(**product.__dict__, in_cart=product_in_cart.quantity)
    await session.commit()
    return product


@router.post("/remove")
async def remove_item_from_cart(
    session: SessionDep,
    user: CurrentUser,
    item: CartItemAdd,
) -> ProductModel:
    product = await session.get(ProductsOrm, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_in_cart = (
        await session.execute(
            select(CartItemsOrm)
            .options(joinedload(CartItemsOrm.product))
            .where(
                CartItemsOrm.user_id == user.id,
                CartItemsOrm.product_id == item.product_id,
            )
        )
    ).scalar_one_or_none()

    if not product_in_cart:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    if product_in_cart.quantity > 1:
        product_in_cart.quantity -= 1
        in_cart = product_in_cart.quantity
    else:
        await session.delete(product_in_cart)
        in_cart = 0

    product = ProductModel(**product.__dict__, in_cart=in_cart)
    await session.commit()
    return product
