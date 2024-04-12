from app.api.deps import CurrentUser, SessionDep
from app.models import CartItemsOrm
from app.models.products import ProductsOrm
from app.schemas.carts import CartItem, CartItemAdd, CartItemRemove, UserCart
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

router = APIRouter()


@router.get("/")
async def get_user_cart(
    session: SessionDep,
    user: CurrentUser,
) -> UserCart:
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
    session: SessionDep, user: CurrentUser, product_to_remove: CartItemRemove
) -> UserCart:
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
