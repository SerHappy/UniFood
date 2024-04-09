document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Предотвратить стандартную отправку формы
    const email = document.getElementById('register_email').value;
    const password = document.getElementById('register_psw').value;
    const passwordRepeat = document.getElementById('psw_repeat').value;

    if (password !== passwordRepeat) {
        alert('Пароли не совпадают');
        return;
    }

    const data = { email, password };

    // Отправляем запрос на регистрацию
    fetch('http://127.0.0.1:8000/api/v1/registration', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
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
            document.querySelector('.success-message').style.display = 'block';
        })
        .catch((error) => {
            console.error('Error:', error);
            alert(`Ошибка: ${error.detail || 'Неизвестная ошибка'}`);
        });
});
