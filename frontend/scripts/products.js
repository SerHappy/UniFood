function fetchData() {
    console.log('Fetching data...');
    const headers = {
        'Content-Type': 'application/json'
    };
    const token = localStorage.getItem('accessToken');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    fetch("http://localhost:8000/api/v1/products/all/", {
        method: 'GET',
        headers: headers
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
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
        createProductCard(product, productsDiv);
    });

    return productsDiv;
}

function createProductCard(product, container) {
    const card = document.createElement('div');
    card.classList.add('card');
    card.dataset.productId = product.product_id;
    drawProductCard(card, product);
    container.appendChild(card);
}

function createAndShowModal(product) {
    const modal = document.createElement('div');
    modal.setAttribute('id', 'productModal');
    modal.style.display = 'block';
    modal.style.position = 'fixed';
    modal.style.textAlign = 'center';
    modal.style.left = '0';
    modal.style.top = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    modal.style.zIndex = '1000';
    modal.style.overflow = 'auto';
    const modalContent = document.createElement('div');
    modalContent.style.backgroundColor = '#fff';
    modalContent.style.margin = '15% auto';
    modalContent.style.padding = '20px';
    modalContent.style.border = '1px solid #888';
    modalContent.style.width = '50%';

    const closeButton = document.createElement('span');
    closeButton.textContent = '×';
    closeButton.style.color = '#aaa';
    closeButton.style.float = 'right';
    closeButton.style.fontSize = '28px';
    closeButton.style.fontWeight = 'bold';
    closeButton.style.cursor = 'pointer';

    closeButton.onclick = function () {
        modal.parentNode.removeChild(modal);
    };

    // Добавление названия товара
    const productName = document.createElement('h3');
    productName.textContent = product.name;
    productName.style.fontFamily = "MursGothic";

    // Добавление описания товара
    const productDescription = document.createElement('p');
    // productDescription.textContent = product.description;
    productDescription.textContent = "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";

    // Сборка всего вместе
    modalContent.appendChild(closeButton);
    modalContent.appendChild(productName);
    modalContent.appendChild(productDescription);
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    modal.addEventListener('click', function (event) {
        if (event.target === modal) { 
            document.body.removeChild(modal);
        }
    });
}


function drawProductCard(card, product) {
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
      ${product.in_cart != 0 ? `<div class="in-cart-capsule">
                <button class="quantity-btn minus">-</button>
                <span class="quantity-number">${product.in_cart}</span>
                <button class="quantity-btn plus">+</button>
            </div>` : `<button class="btn-add-to-cart">В корзину</button>`}
    </div>
  `;
    card.onclick = function () {
        const productId = product.id;
        fetch(`http://localhost:8000/api/v1/products/info/${productId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(productDetails => {
                createAndShowModal(productDetails);
            })
            .catch(error => {
                console.error('Failed to fetch product details:', error);
            });
    };

    card.querySelectorAll('.quantity-btn, .btn-add-to-cart').forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation();  // Останавливает всплытие события к родителю
        });
    });


    const minusButton = card.querySelector('.minus');
    const plusButton = card.querySelector('.plus');
    const addToCartButton = card.querySelector('.btn-add-to-cart');
    if (minusButton) {
        minusButton.onclick = () => RemoveProduct(product.id, card);
    }
    if (plusButton) {
        plusButton.onclick = () => AddProduct(product.id, card);
    }
    if (addToCartButton) {
        addToCartButton.onclick = () => handleAddToCartClick(product, card);
    }
}

function AddProduct(productId, card) {
    console.log('Добавляем в корзину продукт:', productId);
    fetch(`http://localhost:8000/api/v1/products/add`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        },
        body: JSON.stringify({ product_id: productId })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update product quantity');
            }
            return response.json();
        })
        .then(product => {
            // Перерисовка карточки с новыми данными продукта
            drawProductCard(card, product);
        })
        .catch(error => {
            console.error('Error updating product quantity:', error);
        });
}

function RemoveProduct(productId, card) {
    fetch(`http://localhost:8000/api/v1/products/remove`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        },
        body: JSON.stringify({ product_id: productId })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update product quantity');
            }
            return response.json();
        })
        .then(product => {
            drawProductCard(card, product);
        })
        .catch(error => {
            console.error('Error updating product quantity:', error);
        });
}

function handleAddToCartClick(product, card) {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken || isTokenExpired(accessToken)) {
        showModal();
    } else {
        console.log('Добавляем в корзину продукт:', product.name);
        AddProduct(product.id, card);
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
