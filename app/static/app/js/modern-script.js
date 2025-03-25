// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeToasts();
    initializeProductCards();
    initializeNavbar();
});

// Initialize animations for elements
function initializeAnimations() {
    const animatedElements = document.querySelectorAll('.product-card, .category-pill, .btn');
    
    // Create intersection observer for fade-in animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    animatedElements.forEach(el => observer.observe(el));
}

// Toast notification system
function initializeToasts() {
    window.showToast = function(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        document.body.appendChild(toast);

        // Remove toast after 3 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Product card interactions
function initializeProductCards() {
    const cards = document.querySelectorAll('.product-card');
    
    cards.forEach(card => {
        // Add hover effect
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });

        // Quick view functionality
        const quickViewBtn = card.querySelector('.quick-view-btn');
        if (quickViewBtn) {
            quickViewBtn.addEventListener('click', function(e) {
                e.preventDefault();
                const productId = this.dataset.productId;
                showQuickView(productId);
            });
        }
    });
}

// Navbar scroll effect
function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll <= 0) {
            navbar.classList.remove('scroll-up');
            return;
        }

        if (currentScroll > lastScroll && !navbar.classList.contains('scroll-down')) {
            navbar.classList.remove('scroll-up');
            navbar.classList.add('scroll-down');
        } else if (currentScroll < lastScroll && navbar.classList.contains('scroll-down')) {
            navbar.classList.remove('scroll-down');
            navbar.classList.add('scroll-up');
        }
        lastScroll = currentScroll;
    });
}

// Cart functionality
function updateCart(productId, action) {
    fetch(`/update-cart/${productId}/${action}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message);
            updateCartCounter(data.cartCount);
        }
    })
    .catch(error => {
        showToast('Error updating cart', 'error');
    });
}

// Wishlist functionality
function toggleWishlist(productId) {
    fetch(`/toggle-wishlist/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message);
            updateWishlistCounter(data.wishlistCount);
        }
    })
    .catch(error => {
        showToast('Error updating wishlist', 'error');
    });
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Update cart counter in navbar
function updateCartCounter(count) {
    const counter = document.querySelector('.cart-counter');
    if (counter) {
        counter.textContent = count;
        counter.classList.add('pulse');
        setTimeout(() => counter.classList.remove('pulse'), 1000);
    }
}

// Update wishlist counter in navbar
function updateWishlistCounter(count) {
    const counter = document.querySelector('.wishlist-counter');
    if (counter) {
        counter.textContent = count;
        counter.classList.add('pulse');
        setTimeout(() => counter.classList.remove('pulse'), 1000);
    }
}

// Product quick view modal
function showQuickView(productId) {
    fetch(`/product-quick-view/${productId}/`)
        .then(response => response.json())
        .then(data => {
            const modal = document.createElement('div');
            modal.className = 'quick-view-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <span class="close-modal">&times;</span>
                    <div class="product-quick-view">
                        <img src="${data.image}" alt="${data.name}">
                        <div class="product-info">
                            <h2>${data.name}</h2>
                            <p class="price">₹${data.price}</p>
                            <p class="description">${data.description}</p>
                            <button class="btn btn-primary add-to-cart" 
                                    onclick="updateCart(${productId}, 'add')">
                                Add to Cart
                            </button>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);

            // Close modal functionality
            const closeBtn = modal.querySelector('.close-modal');
            closeBtn.onclick = function() {
                modal.remove();
            }

            // Close on outside click
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.remove();
                }
            }
        })
        .catch(error => {
            showToast('Error loading product details', 'error');
        });
}

// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
}); 