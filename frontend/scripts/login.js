document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('login_uname').value;
    const password = document.getElementById('login_psw').value;

    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);

    fetch('http://127.0.0.1:8000/api/v1/auth/login/access-token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data.toString(),
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(error => Promise.reject(error));
            }
        })
        .then(data => {
            console.log('Success:', data);
            localStorage.setItem('accessToken', data.access_token);
            updateNavigationBar();
            closeModal();
        })
        .catch((error) => {
            console.error('Error:', error);
            alert(`Ошибка входа: ${error.detail || 'Неверный логин или пароль или почта не подтверждена'}`);
        });
});

function isTokenExpired(token) {
    const payloadBase64 = token.split('.')[1];
    const decodedJson = atob(payloadBase64);
    const decoded = JSON.parse(decodedJson);
    const exp = decoded.exp; // Время истечения в формате UNIX timestamp
    const now = Date.now() / 1000; // Текущее время в формате UNIX timestamp

    return exp < now;
}

document.addEventListener('DOMContentLoaded', (event) => {
    const accessToken = localStorage.getItem('accessToken');
    console.log('Access token:', accessToken);
    if (accessToken && !isTokenExpired(accessToken)) {
        console.log('Token is valid');
        // Токен найден и он валиден, обновляем навигационное меню
        updateNavigationBar();
        // Закрыть модальное окно входа, если оно открыто
        closeModal();
    } else {
        console.log('Token is missing or expired');
        // Токен отсутствует или истек, очистить локальное хранилище и показать стандартное меню
        localStorage.removeItem('accessToken');
        // Здесь может быть логика для отображения навигации, требующей входа
    }
});

function updateNavigationBar() {
    const navBar = document.querySelector('.top-nav');
    navBar.innerHTML = `
        <a href="#">Очередь заказов</a>
        <a href="#">Акции</a>
        <a href="#">Профиль</a>
        <a href="#">Корзина</a>
    `;
}

function closeModal() {
    // Закрытие модального окна. Этот код зависит от того, как реализовано твоё модальное окно.
    // Например, если ты используешь Bootstrap, это может выглядеть так:
    // $('#modalId').modal('hide');

    // Если модальное окно реализовано через CSS и JavaScript, возможно, тебе понадобится что-то вроде:
    document.getElementById('modal').style.display = 'none';

    // Подставь правильный ID или логику для своего модального окна.
}
