function setupModal() {
    console.log("Setting up modal...");
    const modal = document.getElementById('modal');
    // Получаем кнопку открытия модального окна
    const btnLogin = document.getElementById("modalTrigger");
    // Получаем кнопку для переключения на форму регистрации
    const toRegisterBtn = document.getElementById("toRegister");
    // Получаем все элементы для закрытия модального окна
    const closeSpans = document.getElementsByClassName("close");

    // Проверяем, существует ли кнопка входа, прежде чем назначить обработчик событий
    if (btnLogin) {
        btnLogin.onclick = () => {
            modal.style.display = "flex";
            document.getElementById("loginForm").style.display = "block";
            document.getElementById("registerForm").style.display = "none";
        };
    }

    // Переключение на форму регистрации
    if (toRegisterBtn) {
        toRegisterBtn.onclick = () => {
            document.getElementById("loginForm").style.display = "none";
            document.getElementById("registerForm").style.display = "block";
        };
    }

    // Назначаем обработчики закрытия модального окна
    Array.from(closeSpans).forEach(closeSpan => {
        closeSpan.onclick = () => {
            modal.style.display = "none";
        };
    });

    // Закрытие модального окна при клике вне его области
    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
    console.log("Modal setup complete.");
}
