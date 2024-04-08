"""Fill products and categories

Revision ID: 008bcef16dc4
Revises: 235f011606cf
Create Date: 2024-04-08 14:13:01.264767

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "008bcef16dc4"
down_revision: Union[str, None] = "235f011606cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Вставляем данные
    op.execute(
        """
    INSERT INTO products (name, price, composition, description, weight, photo_url, rating, is_in_stock)
    VALUES
        ('Цезарь с курицей', 270, '', '', 290, 'caesar-s-kuritsey.jpg', NULL, True),
        ('Цезарь с креветкой', 400, '', '', 290, 'caesar-s-krevetkoy.jpg', NULL, True),
        ('Нисуас', 300, '', '', 295, 'nisuas.jpg', NULL, True),
        ('Сендвич с семгой', 250, '', '', 180, 'sendvich-s-semgoy.jpg', NULL, True),
        ('Сендвич с курицей', 160, '', '', 180, 'sendvich-s-kuritsey.jpg', NULL, True),
        ('Сендвич с ветчиной', 160, '', '', 180, 'sendvich-s-vetchinoy.jpg', NULL, True),
        ('Кофе 3в1', 300, '', '', NULL, 'kofe-3v1.jpg', NULL, True),
        ('Американо 200мл', 90, '', '', 200, 'americano-200ml.jpg', NULL, True),
        ('Американо 400мл', 140, '', '', 400, 'americano-400ml.jpg', NULL, True),
        ('Капучино 200мл', 100, '', '', 200, 'kapuchino-200ml.jpg', NULL, True),
        ('Капучино 400мл', 160, '', '', 400, 'kapuchino-400ml.jpg', NULL, True),
        ('Латте 200мл', 100, '', '', 200, 'latte-200ml.jpg', NULL, True),
        ('Латте 400мл', 160, '', '', 400, 'latte-400ml.jpg', NULL, True),
        ('Эспрессо 45мл', 160, '', '', 45, 'espresso-45ml.jpg', NULL, True),
        ('Эспрессо двойной 90 мл', 130, '', '', 90, 'espresso-dvoynoy-90ml.jpg', NULL, True),
        ('Чай 200 мл', 40, '', '', 200, 'chay-200ml.jpg', NULL, True),
        ('Чай 400 мл', 60, '', '', 400, 'chay-400ml.jpg', NULL, True),
        ('Вок вегетарианский', 220, '', '', 225, 'wok-vegetarianskiy.jpg', NULL, True),
        ('Вок с курицей', 250, '', '', 255, 'wok-s-kuritsey.jpg', NULL, True),
        ('Вок с креветками', 290, '', '', 245, 'wok-s-krevetkami.jpg', NULL, True),
        ('Крем суп грибной', 120, '', '', 310, 'krem-sup-gribnoy.jpg', NULL, True),
        ('Спагетти с мидиями', 340, '', '', 360, 'spaghetti-s-midyami.jpg', NULL, True),
        ('Бургер с говядиной', 230, '', '', 250, 'burger-s-govyadinoy.jpg', NULL, True),
        ('Бургер куриный', 190, '', '', 250, 'burger-kuriniy.jpg', NULL, True),
        ('Бургер с куриными стрипсами', 190, '', '', 235, 'burger-s-kurinymi-stripsami.jpg', NULL, True),
        ('Хот дог куриный', 160, '', '', 220, 'hot-dog-kuriniy.jpg', NULL, True),
        ('Шаурма с курицей', 200, '', '', 405, 'shawarma-s-kuritsey.jpg', NULL, True),
        ('Кесадилья с курицей', 185, '', '', 205, 'quesadilla-s-kuritsey.jpg', NULL, True),
        ('Буритто с говядиной', 160, '', '', 165, 'burrito-s-govyadinoy.jpg', NULL, True),
        ('Шаурма в пите', 180, '', '', 255, 'shawarma-v-pite.jpg', NULL, True),
        ('Куриные крылья барбекю', 130, '', '', 250, 'kurinye-krylya-barbekyu.jpg', NULL, True),
        ('Картофель по-деревенски', 80, '', '', 100, 'kartofel-po-derevenski.jpg', NULL, True),
        ('Картофель фри', 80, '', '', 100, 'kartofel-fri.jpg', NULL, True),
        ('Сырные палочки', 110, '', '', 100, 'syrnye-palochki.jpg', NULL, True),
        ('Луковые кольца', 65, '', '', 100, 'lukovye-koltsa.jpg', NULL, True),
        ('Нагетсы куриные', 110, '', '', 100, 'nagetsy-kurinye.jpg', NULL, True),
        ('Спрингролл овощной', 150, '', '', 180, 'springroll-ovoschnoy.jpg', NULL, True),
        ('Спрингролл с креветками', 240, '', '', 150, 'springroll-s-krevetkami.jpg', NULL, True),
        ('Спрингролл с курицей', 210, '', '', 165, 'springroll-s-kuritsey.jpg', NULL, True),
        ('Пицца барбекю', 90, '', '', 115, 'pizza-barbekyu.jpg', NULL, True),
        ('Пицца цезарь с курицей', 90, '', '', 115, 'pizza-caesar-s-kuritsey.jpg', NULL, True),
        ('Пицца пепперони', 90, '', '', 115, 'pizza-pepperoni.jpg', NULL, True),
        ('Пицца ветчина и грибы', 90, '', '', 115, 'pizza-vetchina-i-griby.jpg', NULL, True),
        ('Пицца 4 сыра', 90, '', '', 110, 'pizza-4-syra.jpg', NULL, True),
        ('Пицца Маргарита', 90, '', '', 110, 'pizza-margarita.jpg', NULL, True),
        ('Пирожок с капустой', 50, '', '', 100, 'pirozhok-s-kapustoy.jpg', NULL, True),
        ('Пирожок с картошкой и грибами', 50, '', '', 100, 'pirozhok-s-kartoshkoy-i-gribami.jpg', NULL, True),
        ('Творожное кольцо', 99, '', '', 75, 'tvorozhnoe-koltso.jpg', NULL, True),
        ('Комбо 1', 250, 'ХотДог с курицей, картофель фри или по деревенски, чай/морс', '', NULL, 'combo-1.jpg', NULL, True);
    """
    )
    op.execute(
        """
    INSERT INTO categories (name)
    VALUES
        ('Салаты'),
        ('Сендвичи'),
        ('Напитки'),
        ('Воки'),
        ('Горячие блюда'),
        ('Фастфуд'),
        ('Закуски'),
        ('Спрингроллы'),
        ('Пиццы'),
        ('Выпечка'),
        ('Комбо');
        """
    )
    op.execute(
        """
    INSERT INTO categories_products (category_id, product_id)
    VALUES
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 7),
        (3, 8),
        (3, 9),
        (3, 10),
        (3, 11),
        (3, 12),
        (3, 13),
        (3, 14),
        (3, 15),
        (3, 16),
        (3, 17),
        (4, 18),
        (4, 19),
        (4, 20),
        (5, 21),
        (5, 22),
        (6, 23),
        (6, 24),
        (6, 25),
        (6, 26),
        (6, 27),
        (6, 28),
        (6, 29),
        (6, 30),
        (6, 31),
        (7, 32),
        (7, 33),
        (7, 34),
        (7, 35),
        (7, 36),
        (8, 37),
        (8, 38),
        (8, 39),
        (9, 40),
        (9, 41),
        (9, 42),
        (9, 43),
        (9, 44),
        (9, 45),
        (10, 46),
        (10, 47),
        (10, 48),
        (11, 49);
        """
    )


def downgrade() -> None:
    op.drop_table("products")
    op.drop_table("categories")
    op.drop_table("categories_products")
