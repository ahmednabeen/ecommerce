document.addEventListener('DOMContentLoaded', (event) => {

    // --- Hamburger Menu Functionality ---
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Check if both hamburger and nav-links exist
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // --- Search Bar Functionality ---
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    
    // Check if search elements exist on the page
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

    // --- Shopping Cart Functionality ---
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    const cartBadge = document.getElementById('cartBadge');
    
    // Check if cart elements exist on the page
    if (addToCartButtons.length > 0 && cartBadge) {
        let itemCount = parseInt(cartBadge.textContent) || 0;

        addToCartButtons.forEach(button => {
            button.addEventListener('click', () => {
                itemCount++;
                cartBadge.textContent = itemCount;
                // The 'active' class on the badge is good for animations
                if (!cartBadge.classList.contains('active')) {
                    cartBadge.classList.add('active');
                }
            });
        });
    }
});
