// Animaciones y efectos para la interfaz
document.addEventListener('DOMContentLoaded', function() {
    // Variables para elementos de la interfaz
    const productItems = document.querySelectorAll('.product-item');
    const buttons = document.querySelectorAll('.btn-hover');
    const nav = document.querySelector('nav.nav');
    let lastScrollTop = 0;

    // Animación de entrada para productos
    function animateProducts() {
        productItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                item.style.transition = 'all 0.6s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    // Efecto parallax para imágenes de productos
    function setupParallax() {
        productItems.forEach(item => {
            const img = item.querySelector('img');
            if (img) {
                item.addEventListener('mousemove', (e) => {
                    const { left, top, width, height } = item.getBoundingClientRect();
                    const x = (e.clientX - left) / width - 0.5;
                    const y = (e.clientY - top) / height - 0.5;
                    
                    img.style.transform = `
                        scale(1.1)
                        rotateY(${x * 10}deg)
                        rotateX(${y * -10}deg)
                    `;
                });

                item.addEventListener('mouseleave', () => {
                    img.style.transform = 'scale(1) rotateY(0) rotateX(0)';
                });
            }
        });
    }

    // Efecto de brillo en hover para botones
    function setupButtonEffects() {
        buttons.forEach(button => {
            button.addEventListener('mousemove', (e) => {
                const { left, top, width, height } = button.getBoundingClientRect();
                const x = (e.clientX - left) / width;
                const y = (e.clientY - top) / height;

                button.style.setProperty('--x', x.toFixed(2));
                button.style.setProperty('--y', y.toFixed(2));
            });
        });
    }

    // Navegación con efecto de desvanecimiento
    function handleNavigation() {
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > lastScrollTop) {
                // Scroll hacia abajo
                nav.style.transform = 'translateY(-100%)';
            } else {
                // Scroll hacia arriba
                nav.style.transform = 'translateY(0)';
                nav.style.backgroundColor = currentScroll > 50 ? 'var(--navy-transparent)' : 'transparent';
            }
            
            lastScrollTop = currentScroll;
        });
    }

    // Carrusel automático para productos
    function setupCarousel() {
        const productList = document.querySelector('.product-list');
        if (productList) {
            setInterval(() => {
                productList.scrollBy({
                    left: 300,
                    behavior: 'smooth'
                });

                if (productList.scrollLeft + productList.clientWidth >= productList.scrollWidth) {
                    productList.scrollTo({ left: 0, behavior: 'smooth' });
                }
            }, 5000);
        }
    }

    // Lazy loading para imágenes
    function setupLazyLoading() {
        const images = document.querySelectorAll('.product-item img');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('fade-in');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Notificaciones toast
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Inicializar todas las funcionalidades
    function init() {
        animateProducts();
        setupParallax();
        setupButtonEffects();
        handleNavigation();
        setupCarousel();
        setupLazyLoading();
    }

    init();
}); 