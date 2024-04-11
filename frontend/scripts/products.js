function fetchData() {
    console.log('Fetching data...');
    fetch('http://localhost:8000/api/v1/products/all/')
        .then(response => response.json())
        .then(categories => renderCategories(categories))
        .catch(error => console.error('Ошибка при загрузке данных: ', error));
}

function renderCategories(categories) {
    const navBar = document.querySelector('.bottom-nav');
    const content = document.querySelector("#dynamicContent");
    content.innerHTML = '';
    navBar.innerHTML = '';

    categories.forEach(category => {
        const link = document.createElement('a');
        link.href = `#${category.name}`;
        link.textContent = category.name;
        link.onclick = () => setActiveLink(link);
        navBar.appendChild(link);

        const categorySection = createCategorySection(category);
        content.appendChild(categorySection);
    });

    updateActiveSection();
}

function setActiveLink(link) {
    document.querySelectorAll('.bottom-nav a').forEach(navLink => {
        navLink.classList.remove('active');
    });
    link.classList.add('active');
}

function createCategorySection(category) {
    const section = document.createElement('div');
    section.classList.add('category');
    section.id = category.name;
    section.innerHTML = `<h2>${category.name}</h2>`;
    const productsDiv = createProductsDiv(category.products);
    section.appendChild(productsDiv);
    return section;
}

function createProductsDiv(products) {
    const productsDiv = document.createElement('div');
    productsDiv.classList.add('products');

    products.forEach(product => {
        const productCard = createProductCard(product);
        productsDiv.appendChild(productCard);
    });

    return productsDiv;
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.classList.add('card');
    card.innerHTML = `
    <div class="card-image">
      <img src='./images/Бургер.png' alt="Изображение продукта">
    </div>
    <div class="card-rating">
      <span>${product.rating ? product.rating : 0}</span>
      <img src="./images/pngwing 1.png" alt="Рейтинг">
    </div>
    <div class="card-content">
      <h3 class="dish-name">${product.name}</h3>
      ${product.weight ? `<p class="dish-weight">${product.weight}гр</p>` : ''}
      <span class="dish-price">${product.price}</span>
      <button class="btn-add-to-cart">В корзину</button>
    </div>
  `;
    const addToCartButton = card.querySelector('.btn-add-to-cart');
    addToCartButton.onclick = () => handleAddToCartClick(product);
    return card;
}

function handleAddToCartClick(product) {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken || isTokenExpired(accessToken)) {
        // Если пользователь не авторизован или токен истек, показываем модальное окно входа
        showModal();
    } else {
        // Пользователь авторизован, логика добавления в корзину
        console.log('Добавляем в корзину продукт:', product.name);
        // Здесь должна быть реализация добавления товара в корзину
    }
}

function showModal() {
    const modal = document.getElementById('modal'); // Используй реальный ID модального окна
    if (modal) {
        modal.style.display = 'flex'; // Или другой способ показа, зависящий от твоей реализации
        document.getElementById("loginForm").style.display = "block";
        document.getElementById("registerForm").style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    setupModal();
    fetchData();
    window.addEventListener('scroll', updateActiveSection);
    document.getElementById('MenuLink').addEventListener('click', (e) => {
        console.log('Клик по ссылке "Меню"');
        e.preventDefault();
        fetchData();
    });
});
