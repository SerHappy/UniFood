import uuid
from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from yookassa import Payment

from app.api.deps import CurrentUser, SessionDep
from app.models import CartItemsOrm
from app.models.products import ProductsOrm
from app.schemas.carts import CartItem, CartItemAdd, CartItemRemove, UserCart

router = APIRouter()


@router.get("/")
async def get_user_cart(
    session: SessionDep,
    user: CurrentUser,
) -> UserCart:
    """Эндпоинт для получения корзины пользователя.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param user: Зависимость для получения пользователя.
    :type user: CurrentUser
    :return: Схема Pydantic корзины пользователя.
    :rtype: UserCart
    """
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

    items = [
        CartItem(
            product_id=cart_item_orm.product.id,
            name=cart_item_orm.product.name,
            price_per_one=cart_item_orm.product.price,
            weight=cart_item_orm.product.weight,
            full_price=cart_item_orm.product.price * cart_item_orm.quantity,
            photo_url=cart_item_orm.product.photo_url,
            quantity=cart_item_orm.quantity,
        )
        for cart_item_orm in cart_items_orm
    ]

    total = sum(item.full_price for item in items)
    discount = 0
    to_pay = total - discount

    return UserCart(
        id=user.id, items=items, total=total, discount=discount, to_pay=to_pay
    )


@router.post("/add")
async def add_to_cart(
    session: SessionDep,
    user: CurrentUser,
    item: CartItemAdd,
) -> UserCart:
    """Эндпоинт для добавления продукта в корзину.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param user: Зависимость для получения пользователя.
    :type user: CurrentUser
    :param item: Схема Pydantic продукта для добавления в корзину.
    :type item: CartItemAdd
    :raises HTTPException: Ошибка добавления в корзину, если продукта нет в базе.
    :return: Схема Pydantic корзины пользователя.
    :rtype: UserCart
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

    items = [
        CartItem(
            product_id=cart_item_orm.product.id,
            name=cart_item_orm.product.name,
            price_per_one=cart_item_orm.product.price,
            weight=cart_item_orm.product.weight,
            full_price=cart_item_orm.product.price * cart_item_orm.quantity,
            photo_url=cart_item_orm.product.photo_url,
            quantity=cart_item_orm.quantity,
        )
        for cart_item_orm in cart_items_orm
    ]

    total = sum(item.full_price for item in items)
    discount = 0
    to_pay = total - discount

    cart = UserCart(
        id=user.id, items=items, total=total, discount=discount, to_pay=to_pay
    )
    await session.commit()
    return cart


@router.post("/remove")
async def remove_from_cart(
    session: SessionDep,
    user: CurrentUser,
    product_to_remove: CartItemRemove,
) -> UserCart:
    """Эндпоинт для уменьшения продукта в корзине.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param user: Зависимость для получения пользователя.
    :type user: CurrentUser
    :param product_to_remove: Схема Pydantic продукта для удаления из корзины.
    :type product_to_remove: CartItemRemove
    :raises HTTPException: Ошибка удаления из корзины, если продукта нет в корзине.
    :return: Схема Pydantic корзины пользователя.
    :rtype: UserCart
    """
    product = await session.get(ProductsOrm, product_to_remove.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_in_cart = (
        await session.execute(
            select(CartItemsOrm).where(
                CartItemsOrm.user_id == user.id,
                CartItemsOrm.product_id == product_to_remove.product_id,
            )
        )
    ).scalar_one_or_none()
    if not product_in_cart:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    if product_in_cart.quantity > 1:
        product_in_cart.quantity -= 1
    else:
        await session.delete(product_in_cart)
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

    items = [
        CartItem(
            product_id=cart_item_orm.product.id,
            name=cart_item_orm.product.name,
            price_per_one=cart_item_orm.product.price,
            weight=cart_item_orm.product.weight,
            full_price=cart_item_orm.product.price * cart_item_orm.quantity,
            photo_url=cart_item_orm.product.photo_url,
            quantity=cart_item_orm.quantity,
        )
        for cart_item_orm in cart_items_orm
    ]

    total = sum(item.full_price for item in items)
    discount = 0
    to_pay = total - discount

    cart = UserCart(
        id=user.id, items=items, total=total, discount=discount, to_pay=to_pay
    )
    await session.commit()
    return cart


@router.delete("/delete")
async def delete_from_cart(
    session: SessionDep,
    user: CurrentUser,
    product_to_remove: CartItemRemove,
) -> UserCart:
    """Эндпоинт для удаления продукта из корзины.

    :param session: Зависимость для работы с сессиями базы данных.
    :type session: SessionDep
    :param user: Зависимость для получения пользователя.
    :type user: CurrentUser
    :param product_to_remove: Схема Pydantic продукта для удаления из корзины.
    :type product_to_remove: CartItemRemove
    :raises HTTPException: Ошибка удаления из корзины, если продукта нет в базе.
    :return: Схема Pydantic корзины пользователя.
    :rtype: UserCart
    """
    product = await session.get(ProductsOrm, product_to_remove.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_in_cart = (
        await session.execute(
            select(CartItemsOrm).where(
                CartItemsOrm.user_id == user.id,
                CartItemsOrm.product_id == product_to_remove.product_id,
            )
        )
    ).scalar_one_or_none()
    if not product_in_cart:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    await session.delete(product_in_cart)
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

    items = [
        CartItem(
            product_id=cart_item_orm.product.id,
            name=cart_item_orm.product.name,
            price_per_one=cart_item_orm.product.price,
            weight=cart_item_orm.product.weight,
            full_price=cart_item_orm.product.price * cart_item_orm.quantity,
            photo_url=cart_item_orm.product.photo_url,
            quantity=cart_item_orm.quantity,
        )
        for cart_item_orm in cart_items_orm
    ]

    total = sum(item.full_price for item in items)
    discount = 0
    to_pay = total - discount

    cart = UserCart(
        id=user.id, items=items, total=total, discount=discount, to_pay=to_pay
    )
    await session.commit()
    return cart


@router.post("/checkout")
async def checkout(
    session: SessionDep,
    user: CurrentUser,
):
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

    items = [
        CartItem(
            product_id=cart_item_orm.product.id,
            name=cart_item_orm.product.name,
            price_per_one=cart_item_orm.product.price,
            weight=cart_item_orm.product.weight,
            full_price=cart_item_orm.product.price * cart_item_orm.quantity,
            photo_url=cart_item_orm.product.photo_url,
            quantity=cart_item_orm.quantity,
        )
        for cart_item_orm in cart_items_orm
    ]

    total = sum(item.full_price for item in items)
    discount = 0
    to_pay = total - discount

    cart = UserCart(
        id=user.id,
        items=items,
        total=total,
        discount=discount,
        to_pay=to_pay,
    )

    payment = Payment.create(
        {
            "amount": {"value": cart.to_pay, "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "https://www.example.com/return_url",
            },
            "capture": True,
            "description": "Заказ №1",
        },
        uuid.uuid4(),
    )

    return RedirectResponse(
        url=payment.confirmation.confirmation_url,  # type: ignore
        status_code=status.HTTP_303_SEE_OTHER,
    )
