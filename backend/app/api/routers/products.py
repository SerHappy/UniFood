from collections.abc import Sequence

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.api.deps import CurrentOptionalUser, CurrentUser, SessionDep
from app.models import CategoriesOrm, CategoriesProductsOrm, ProductsOrm
from app.models.cart_items import CartItemsOrm
from app.schemas.carts import CartItemAdd, CartItemRemove
from app.schemas.items import CategoryModel, ProductInfo, ProductModel

router = APIRouter()


@router.get("/all/", response_model=list[CategoryModel])
async def read_categories_with_products(
    session: SessionDep,
    user: CurrentOptionalUser,
) -> list[CategoryModel]:
    """Эндпоинт для получения категорий с продуктами.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param user: Зависимость для получения пользователя.
    :type user: CurrentOptionalUser
    :return: Список Pydantic схем категорий с продуктами.
    :rtype: list[CategoryModel]
    """
    select_query = select(CategoriesOrm)
    categories: Sequence[CategoriesOrm] = (
        (await session.execute(select_query)).scalars().all()
    )
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
        products: Sequence[ProductsOrm] = (await session.execute(query)).scalars().all()

        if user:
            cart_items_orm: Sequence[CartItemsOrm] = (
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
    """Эндпоинт для получения информации о продукте.

    :param product_id: Идентификатор продукта.
    :type product_id: int
    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :raises HTTPException: Ошибки при получении информации о продукте.
    :return: Схема Pydantic с информацией о продукте.
    :rtype: ProductInfo
    """
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
    """Эндпоинт для добавления продукта в корзину.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param user: Зависимость для получения пользователя.
    :type user: CurrentUser
    :param item: Схема Pydantic продукта для добавления в корзину.
    :type item: CartItemAdd
    :raises HTTPException: Ошибка добавления в корзину, если продукта нет в базе.
    :return: Схема Pydantic продукта.
    :rtype: ProductModel
    """
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

    product_model = ProductModel(**product.__dict__, in_cart=product_in_cart.quantity)  # type: ignore
    await session.commit()
    return product_model


@router.post("/remove")
async def remove_item_from_cart(
    session: SessionDep,
    user: CurrentUser,
    item: CartItemRemove,
) -> ProductModel:
    """Эндпоинт для удаления продукта из корзины.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param user: Зависимость для получения пользователя.
    :type user: CurrentUser
    :param item: Схема Pydantic продукта для удаления из корзины.
    :type item: CartItemRemove
    :raises HTTPException: Ошибка удаления из корзины, если продукта нет в базе.
    :return: Схема Pydantic продукта.
    :rtype: ProductModel
    """
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

    product_model = ProductModel(**product.__dict__, in_cart=in_cart)  # type: ignore
    await session.commit()
    return product_model
