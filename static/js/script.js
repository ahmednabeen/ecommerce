document.addEventListener('DOMContentLoaded', (event) => {

    // --- Sticky Navbar on Scroll ---
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            // If user scrolls down more than 50 pixels
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
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
                // Move input before the button in the HTML structure
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
                if (!cartBadge.classList.contains('active')) {
                    cartBadge.classList.add('active');
                }
            });
        });
    }
});