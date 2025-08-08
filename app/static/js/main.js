// Mobile Menu Functionality
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileNav = document.getElementById('mobileNav');
const mobileCloseBtn = document.getElementById('mobileCloseBtn');
const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

// Toggle mobile menu
mobileMenuBtn.addEventListener('click', () => {
    mobileMenuBtn.classList.toggle('active');
    mobileNav.classList.toggle('active');
    document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : '';
});

// Close mobile menu when clicking on links
mobileNavLinks.forEach(link => {
    link.addEventListener('click', () => {
        mobileMenuBtn.classList.remove('active');
        mobileNav.classList.remove('active');
        document.body.style.overflow = '';
    });
});

// Close mobile menu when clicking close button
mobileCloseBtn.addEventListener('click', () => {
    mobileMenuBtn.classList.remove('active');
    mobileNav.classList.remove('active');
    document.body.style.overflow = '';
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (!mobileMenuBtn.contains(e.target) && !mobileNav.contains(e.target)) {
        mobileMenuBtn.classList.remove('active');
        mobileNav.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Telegram Bot Configuration
// Настроено для отправки сообщений в Telegram

// Apple-style Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Add different animations based on element type
            if (entry.target.classList.contains('collection-card')) {
                entry.target.classList.add('animate');
            } else if (entry.target.classList.contains('section-title')) {
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
            } else if (entry.target.classList.contains('about-text')) {
                entry.target.style.animation = 'slideInFromLeft 0.8s ease-out forwards';
            } else {
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
            }
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements with data-aos attribute
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('[data-aos]');
    animatedElements.forEach(el => {
        observer.observe(el);
    });

    // Initialize smooth scrolling for navigation links
    initSmoothScrolling();
    
    // Initialize form handling
    initContactForm();
    
    // Initialize hover effects
    initHoverEffects();
    
    // Initialize navbar scroll effect
    initNavbarScroll();
    

});

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Contact form handling
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const tgName = this.querySelector('input').value.trim();
            const message = this.querySelector('textarea').value.trim();
            
            // Создаем FormData для отправки данных
            const formData = new FormData();
            formData.append('telegram', tgName);
            formData.append('message', message);

            fetch('/send-message', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('formMessage').style.display = 'block';
                    document.getElementById('formMessage').textContent = data.message;
                    this.reset();
                    setTimeout(() => {
                        document.getElementById('formMessage').style.display = 'none';
                    }, 4000);
                } else {
                    alert('Ошибка отправки: ' + data.message);
                }
            })
            .catch(() => {
                alert('Ошибка отправки. Попробуйте позже.');
            });
        });
    }
}

// Hover effects for collection cards
function initHoverEffects() {
    const collectionCards = document.querySelectorAll('.collection-card');
    
    collectionCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
        
        // Add click effect for better UX
        card.addEventListener('click', () => {
            card.style.transform = 'scale(0.98)';
            setTimeout(() => {
                card.style.transform = 'translateY(-10px)';
            }, 150);
        });
    });
}

// Navbar background on scroll
function initNavbarScroll() {
    const navbar = document.querySelector('.nav');
    if (!navbar) return;
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(0, 0, 0, 0.9)';
        } else {
            navbar.style.background = 'rgba(0, 0, 0, 0.1)';
        }
    });
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimize scroll events
const optimizedScrollHandler = debounce(() => {
    // Scroll-based animations can be added here
}, 10);

window.addEventListener('scroll', optimizedScrollHandler);

// Apple-style loading animation for images
function initImageLoading() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        // Set transition first
        img.style.transition = 'opacity 0.6s ease';
        
        // Check if image is already loaded
        if (img.complete && img.naturalHeight !== 0) {
            // Image is already loaded, show it immediately
            img.style.opacity = '1';
        } else {
            // Image is not loaded yet, set initial state and add listeners
            img.style.opacity = '0';
            
            img.addEventListener('load', () => {
                img.style.opacity = '1';
            });
        }
        
        img.addEventListener('error', () => {
            img.style.opacity = '1';
            img.style.background = '#f0f0f0';
            img.style.display = 'flex';
            img.style.alignItems = 'center';
            img.style.justifyContent = 'center';
            img.style.color = '#666';
            img.style.fontSize = '14px';
            img.innerHTML = 'Изображение не найдено';
        });
    });
    
    // Handle picture elements for WebP support
    const pictures = document.querySelectorAll('picture');
    pictures.forEach(picture => {
        const img = picture.querySelector('img');
        if (img) {
            // Set transition first
            img.style.transition = 'opacity 0.6s ease';
            
            // Check if image is already loaded
            if (img.complete && img.naturalHeight !== 0) {
                // Image is already loaded, show it immediately
                img.style.opacity = '1';
            } else {
                // Image is not loaded yet, set initial state and add listeners
                img.style.opacity = '0';
                
                img.addEventListener('load', () => {
                    img.style.opacity = '1';
                });
            }
            
            img.addEventListener('error', () => {
                img.style.opacity = '1';
                img.style.background = '#f0f0f0';
                img.style.display = 'flex';
                img.style.alignItems = 'center';
                img.style.justifyContent = 'center';
                img.style.color = '#666';
                img.style.fontSize = '14px';
                img.innerHTML = 'Изображение не найдено';
            });
        }
    });
}

// Initialize image loading
document.addEventListener('DOMContentLoaded', initImageLoading);

// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        // Close mobile menu
        mobileMenuBtn.classList.remove('active');
        mobileNav.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Add touch support for mobile devices
function initTouchSupport() {
    const touchElements = document.querySelectorAll('.collection-card, .cta-button');
    
    touchElements.forEach(element => {
        element.addEventListener('touchstart', () => {
            element.style.transform = 'scale(0.98)';
        });
        
        element.addEventListener('touchend', () => {
            element.style.transform = '';
        });
    });
}

// Initialize touch support
document.addEventListener('DOMContentLoaded', initTouchSupport);

// Performance optimization: Lazy loading for images
function initLazyLoading() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', initLazyLoading);

// Mobile-specific image optimization
function optimizeForMobile() {
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        // Only preload the main hero image for each page
        const currentPage = window.location.pathname;
        let imageToPreload = null;
        
        if (currentPage.includes('acne.html')) {
            imageToPreload = 'img/tshirt1.png';
        } else if (currentPage.includes('zip.html')) {
            imageToPreload = 'img/zip1.jpeg';
        }
        
        if (imageToPreload) {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = imageToPreload;
            document.head.appendChild(link);
        }
        
        // Add fetchpriority to all images
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            img.setAttribute('fetchpriority', 'high');
        });
    }
}

// Initialize mobile optimization
document.addEventListener('DOMContentLoaded', optimizeForMobile);

// Mobile Product Gallery Slider
function initMobileGallery() {
    const galleries = document.querySelectorAll('.mobile-product-gallery');
    
    galleries.forEach(gallery => {
        const slides = gallery.querySelectorAll('.mobile-gallery-slide');
        const dots = gallery.querySelectorAll('.mobile-gallery-dot');
        const prevBtn = gallery.querySelector('.mobile-gallery-prev');
        const nextBtn = gallery.querySelector('.mobile-gallery-next');
        
        let currentSlide = 0;
        
        function showSlide(index) {
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            
            slides[index].classList.add('active');
            dots[index].classList.add('active');
        }
        
        function nextSlide() {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        }
        
        function prevSlide() {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            showSlide(currentSlide);
        }
        
        // Event listeners
        if (nextBtn) nextBtn.addEventListener('click', nextSlide);
        if (prevBtn) prevBtn.addEventListener('click', prevSlide);
        
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                currentSlide = index;
                showSlide(currentSlide);
            });
        });
        
        // Touch/swipe support
        let startX = 0;
        let endX = 0;
        
        gallery.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });
        
        gallery.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            const diff = startX - endX;
            
            if (Math.abs(diff) > 50) { // Minimum swipe distance
                if (diff > 0) {
                    nextSlide(); // Swipe left
                } else {
                    prevSlide(); // Swipe right
                }
            }
        });
    });
}

// Initialize mobile gallery
document.addEventListener('DOMContentLoaded', initMobileGallery); 