const API_URL = 'http://localhost:8000/api/v1/cart/';
const HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
};

async function loadCart() {
    if (!HEADERS['Authorization']) {
        console.log('Токен доступа отсутствует. Необходима авторизация.');
        showModal();
        return;
    }

    try {
        const response = await fetch(API_URL, { method: 'GET', headers: HEADERS });
        if (!response.ok) {
            throw new Error(`Ошибка сервера: ${response.statusText}`);
        }
        const cart = await response.json();
        renderCart(cart);
    } catch (error) {
        console.error('Ошибка при загрузке данных корзины: ', error.message);
    }
}

function renderCart(cart) {
    const content = document.querySelector("#dynamicContent");
    const navBar = document.querySelector('.bottom-nav');
    content.innerHTML = '';
    navBar.innerHTML = '';
    const orderPage = document.createElement('div');
    orderPage.className = 'order-page';
    content.appendChild(orderPage);

    const table = document.createElement('table');
    table.className = 'order-items';
    table.innerHTML = getTableHeadersHTML();
    orderPage.appendChild(table);

    const tbody = document.createElement('tbody');
    if (cart.items.length === 0) {
        const emptyRow = document.createElement('tr');
        emptyRow.innerHTML = `<td colspan="5" class="empty-cart">В вашей корзине пусто</td>`;
        tbody.appendChild(emptyRow);
    } else {
        cart.items.forEach(item => {
            tbody.appendChild(createTableRow(item));
        });
    }
    table.appendChild(createTableFooter(cart.total, cart.discount, cart.to_pay));
    table.appendChild(tbody);

    orderPage.appendChild(createOrderParams());

    content.appendChild(orderPage);
}

function getTableHeadersHTML() {
    return `
        <thead>
            <tr>
                <th class="image-col"></th>
                <th class="name-col">Наименование</th>
                <th class="price-col">Цена</th>
                <th class="quantity-col">Количество</th>
                <th class="total-col">Стоимость</th>
                <th class="delete-col"></th>
            </tr>
        </thead>
    `;
}

function createTableRow(item) {
    const row = document.createElement('tr');
    item.photo_url = "./images/Бургер.png";
    row.innerHTML = `
        <td class="item-image"><img src="${item.photo_url}" alt="${item.name}"></td>
        <td class="name">
            <span class="name-title">${item.name}</span>
            <span class="name-weight">${item.weight}гр</span>
        </td>
        <td class="price">${item.price_per_one}₽</td>
        <td>
            <div class="quantity-capsule">
                <button class="quantity-btn minus">-</button>
                <span class="quantity-number">${item.quantity}</span>
                <button class="quantity-btn plus">+</button>
            </div>
        </td>
        <td class="total">${item.full_price}₽</td>
        <td class="delete"><img class="delete-btn" src="./images/ic_delete_48px.png" alt="Удалить"/></td>
    `;
    row.querySelector('.minus').onclick = () => updateCartItem(item.product_id, -1);
    row.querySelector('.plus').onclick = () => updateCartItem(item.product_id, 1);
    row.querySelector('.delete-btn').onclick = () => deleteCartItem(item.product_id);
    return row;
}

function deleteCartItem(productId) {
    fetch(`${API_URL}delete`, { method: 'DELETE', headers: HEADERS, body: JSON.stringify({ product_id: productId }) })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update cart');
            }
            return response.json();
        })
        .then(updatedCart => {
            renderCart(updatedCart);
        })
        .catch(error => {
            console.error('Error updating cart:', error);
        });
}
function updateCartItem(productId, change) {
    const endpoint = change === -1 ? 'remove' : 'add';
    fetch(`${API_URL}${endpoint}`, { method: 'POST', headers: HEADERS, body: JSON.stringify({ product_id: productId }) })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update cart');
            }
            return response.json();
        })
        .then(updatedCart => {
            renderCart(updatedCart);  // Перерисовка всей корзины с новыми данными
        })
        .catch(error => {
            console.error('Error updating cart:', error);
        });
}

function createTableFooter(total, discount, toPay) {
    const tfoot = document.createElement('tfoot');
    tfoot.innerHTML = `
        <tr class="summary total no-border">
            <td class="summary-name" colspan="4">Итого:</td>
            <td class="summary-data" colspan="1">${total}₽</td>
        </tr>
        <tr class="summary discount no-border orange-text">
            <td class="summary-name" colspan="4">Скидка:</td>
            <td class="summary-data" colspan="1">${discount}₽</td>
        </tr>
        <tr class="summary to-pay no-border">
            <td class="summary-name" colspan="4">К оплате:</td>
            <td class="summary-data" colspan="1">${toPay}₽</td>
        </tr>
    `;
    return tfoot;
}

function createOrderParams() {
    const orderParams = document.createElement('div');
    orderParams.className = 'order-params';
    orderParams.innerHTML = `
        <h2>Параметры заказа</h2>
        <div class="button-group">
            <button class="toggle-button active">На месте</button>
            <button class="toggle-button">С собой</button>
        </div>
        <div class="param cook">
            <label for="preparation">Приготовить</label>
            <select id="preparation" class="preparation-select">
                <option>Как можно скорее</option>
                <option>Ко времени</option>
            </select>
        </div>
        <div class="param time-select">
            <label for="time">Выберите время</label>
            <select id="time">
                <option>13:00</option>
                <option>14:00</option>
            </select>
        </div>
        <label for="comments">Комментарий</label>
        <textarea id="comments" rows="4"></textarea>
        <button class="submit">Оформить заказ</button>
    `;
    return orderParams;
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('cartLink').addEventListener('click', (e) => {
        console.log('Клик по ссылке "Корзина"');
        e.preventDefault();
        loadCart();
    });
});
