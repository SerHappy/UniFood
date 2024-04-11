function loadCart() {
    const accessToken = localStorage.getItem('accessToken'); // Получаем токен из localStorage
    if (!accessToken) {
        console.log('Токен доступа отсутствует. Необходима авторизация.');
        showModal(); // Показываем модальное окно для входа или регистрации
        return; // Прерываем функцию, если токен не найден
    }

    // URL API для загрузки данных корзины
    const url = 'http://localhost:8000/api/v1/cart/';

    // Опции запроса
    const options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}` // Добавляем токен в заголовок
        },
        // Если требуется отправить данные, используем body: JSON.stringify(data)
    };

    // Выполнение запроса с помощью fetch API
    fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка получения данных корзины');
            }
            return response.json();
        })
        .then(cart => renderCart(cart))
        .catch(error => {
            console.error('Ошибка при загрузке данных корзины: ', error);
            // Можно также обработать ошибку авторизации, если токен истёк
        });
}

function renderCart(cart) {
    const content = document.querySelector("#dynamicContent");
    const navBar = document.querySelector('.bottom-nav');
    navBar.innerHTML = '';
    content.innerHTML = '';
    // Представление содержимого корзины
    const cartDiv = document.createElement('div');
    cartDiv.innerHTML = '<h1>Корзина</h1>';
    // cart.items.forEach(item => {
    //     const itemElement = document.createElement('div');
    //     itemElement.textContent = `Товар: ${item.name}, Количество: ${item.quantity}`;
    //     cartDiv.appendChild(itemElement);
    // });
    // jsonItems = JSON.stringify(cart.items);
    content.appendChild(cart);
}
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('cartLink').addEventListener('click', (e) => {
        console.log('Клик по ссылке "Корзина"');
        e.preventDefault();
        loadCart();
    });
})
