// -------- CSRF HELPER (ONLY ONCE) --------
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {

    // -------- Hamburger Menu --------
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // -------- Search Bar --------
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    if (searchBtn && searchInput) {
        const searchContainer = searchInput.parentElement;
        searchBtn.addEventListener('click', () => {
            const isActive = searchInput.classList.toggle('active');
            if (isActive) {
                searchInput.focus();
                searchContainer.insertBefore(searchInput, searchBtn);
            }
        });
    }

    // =================================================
    // ✅ REAL ADD TO CART (FIXED)
    // =================================================
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    const cartBadge = document.getElementById('cartBadge');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', () => {

            const productId = button.dataset.productId;

            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: new URLSearchParams({
                    'quantity': 1
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    let currentCount = parseInt(cartBadge.textContent) || 0;
                    cartBadge.textContent = currentCount + 1;
                    cartBadge.classList.add('active');
                }
            })
            .catch(error => console.error('Add to cart error:', error));
        });
    });

    // =================================================
    // ✅ CART DETAIL PAGE – QUANTITY UPDATE (UNCHANGED)
    // =================================================
    const allQuantitySelectors = document.querySelectorAll('.quantity-selector');

    if (allQuantitySelectors.length > 0) {

        function updateCartOnServer(productId, newQuantity) {
            fetch('/cart/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: newQuantity
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'success') {
                    console.error('Cart update failed:', data.message);
                }
            })
            .catch(error => console.error('Update error:', error));
        }

        allQuantitySelectors.forEach(selector => {
            const minusBtn = selector.querySelector('.minus');
            const plusBtn = selector.querySelector('.plus');
            const quantityInput = selector.querySelector('.quantity-input');
            const cartItemCard = selector.closest('.cart-item-card');
            const productId = cartItemCard.dataset.productId;

            minusBtn.addEventListener('click', () => {
                let qty = parseInt(quantityInput.value);
                if (qty > 1) {
                    qty--;
                    quantityInput.value = qty;
                    updateCartOnServer(productId, qty);
                }
            });

            plusBtn.addEventListener('click', () => {
                let qty = parseInt(quantityInput.value);
                qty++;
                quantityInput.value = qty;
                updateCartOnServer(productId, qty);
            });
        });
    }
});

// =================================================
// ✅ REMOVE ITEM FROM CART
// =================================================
const deleteButtons = document.querySelectorAll('.delete-item-btn');

deleteButtons.forEach(button => {
    button.addEventListener('click', () => {

        const cartItemCard = button.closest('.cart-item-card');
        const productId = cartItemCard.dataset.productId;

        fetch('/cart/remove/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                product_id: productId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                cartItemCard.closest('.cart-shop-group').remove();

                // Update badge
                const cartBadge = document.getElementById('cartBadge');
                let count = parseInt(cartBadge.textContent) || 0;
                cartBadge.textContent = Math.max(count - 1, 0);

                if (cartBadge.textContent === '0') {
                    cartBadge.classList.remove('active');
                }
            }
        })
        .catch(err => console.error('Delete error:', err));
    });
});