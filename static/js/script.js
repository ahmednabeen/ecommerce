// ================= CSRF HELPER =================
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

    // ================= HAMBURGER =================
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // ================= SEARCH =================
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', () => {
            searchInput.classList.toggle('active');
            searchInput.focus();
        });
    }

    // ================= ADD TO CART =================
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.dataset.productId;

            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                body: new URLSearchParams({ quantity: 1 })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    const badge = document.getElementById('cartBadge');
                    let count = parseInt(badge.textContent) || 0;
                    badge.textContent = count + 1;
                    badge.classList.add('active');
                }
            });
        });
    });

    // ================= QUANTITY UPDATE =================
    document.querySelectorAll('.quantity-selector').forEach(selector => {
        const minus = selector.querySelector('.minus');
        const plus = selector.querySelector('.plus');
        const input = selector.querySelector('.quantity-input');
        const productId = selector.closest('.cart-item-card').dataset.productId;

        function update(qty) {
            fetch('/cart/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ product_id: productId, quantity: qty })
            });
        }

        minus?.addEventListener('click', () => {
            let qty = parseInt(input.value);
            if (qty > 1) {
                input.value = --qty;
                update(qty);
            }
        });

        plus?.addEventListener('click', () => {
            let qty = parseInt(input.value) + 1;
            input.value = qty;
            update(qty);
        });
    });

    // ================= UPDATE ORDER SUMMARY =================
    function updateOrderSummary() {
        const items = document.querySelectorAll('.cart-item-card');
        const subtotalEl = document.getElementById('subtotal-price');
        const shippingEl = document.getElementById('shipping-fee');
        const totalEl = document.getElementById('grand-total');
        const checkoutBtn = document.getElementById('checkout-btn');

        if (items.length === 0) {
            subtotalEl.textContent = '৳0';
            shippingEl.textContent = '৳0';
            totalEl.textContent = '৳0';
            if (checkoutBtn) checkoutBtn.disabled = true;
        } else {
            let subtotal = 0;
            items.forEach(item => {
                const price = parseFloat(item.querySelector('.item-price').dataset.price);
                const qty = parseInt(item.querySelector('.quantity-input').value);
                subtotal += price * qty;
            });
            subtotalEl.textContent = `৳${subtotal}`;
            const shipping = subtotal > 0 ? 495 : 0;
            shippingEl.textContent = `৳${shipping}`;
            totalEl.textContent = `৳${subtotal + shipping}`;
            if (checkoutBtn) checkoutBtn.disabled = false;
        }
    }

    // ================= SINGLE DELETE =================
    document.querySelectorAll('.delete-item-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const card = btn.closest('.cart-item-card');
            const productId = card.dataset.productId;

            fetch('/cart/remove/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ product_id: productId })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    card.closest('.cart-shop-group').remove();
                    updateOrderSummary();

                    // Update badge
                    const badge = document.getElementById('cartBadge');
                    let count = parseInt(badge.textContent) || 0;
                    badge.textContent = Math.max(count - 1, 0);
                    if (badge.textContent === '0') badge.classList.remove('active');
                }
            });
        });
    });

    // ================= SELECT ALL =================
    const selectAll = document.getElementById('select-all');
    if (selectAll) {
        selectAll.addEventListener('change', function () {
            document.querySelectorAll('.item-select').forEach(cb => {
                cb.checked = this.checked;
            });
        });
    }

    // ================= TOP DELETE (SELECTED) =================
    const topDeleteBtn = document.querySelector('.delete-btn');
    if (topDeleteBtn) {
        topDeleteBtn.addEventListener('click', () => {

            const checked = document.querySelectorAll('.item-select:checked');
            if (checked.length === 0) {
                alert('Select at least one item');
                return;
            }

            const productIds = [...checked].map(cb => cb.dataset.productId);

            fetch('/cart/remove-selected/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ product_ids: productIds })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    checked.forEach(cb => cb.closest('.cart-shop-group').remove());
                    updateOrderSummary();

                    // Update badge
                    const badge = document.getElementById('cartBadge');
                    let count = parseInt(badge.textContent) || 0;
                    count -= checked.length;
                    badge.textContent = Math.max(count, 0);
                    if (badge.textContent === '0') badge.classList.remove('active');
                }
            });
        });
    }

});

    // ================= TOP DELETE (SELECTED) =================

   const backToTopBtn = document.getElementById("backToTop");
        window.onscroll = function () {
        if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        backToTopBtn.style.display = "block";
        } else {
        backToTopBtn.style.display = "none";
        }
        };
        backToTopBtn.onclick = function () {
        window.scrollTo({
        top: 0,
        behavior: "smooth"
        });
        };     