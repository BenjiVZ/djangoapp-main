class SmoothCarousel {
    constructor(element, options = {}) {
        this.container = element;
        this.options = {
            speed: options.speed || 0.5,
            autoplay: options.autoplay !== false,
            pauseOnHover: options.pauseOnHover !== false,
            interval: options.interval || 5000
        };

        this.init();
    }

    init() {
        // Clonar los primeros elementos para scroll infinito
        const items = this.container.children;
        const itemWidth = items[0].offsetWidth;
        const clones = Array.from(items).slice(0, 3).map(item => item.cloneNode(true));
        
        clones.forEach(clone => this.container.appendChild(clone));

        // Variables de control
        let scrollPos = 0;
        let isHovered = false;
        let animationFrame;
        let lastTime = 0;

        // Función de animación suave
        const animate = (currentTime) => {
            if (!lastTime) lastTime = currentTime;
            const delta = currentTime - lastTime;
            
            if (!isHovered && this.options.autoplay) {
                scrollPos += (this.options.speed * delta) / 16;

                // Reset cuando llegamos al final
                if (scrollPos >= (items.length * itemWidth)) {
                    scrollPos = 0;
                }

                this.container.scrollLeft = scrollPos;
            }

            lastTime = currentTime;
            animationFrame = requestAnimationFrame(animate);
        };

        // Iniciar animación
        animationFrame = requestAnimationFrame(animate);

        // Eventos de hover
        if (this.options.pauseOnHover) {
            this.container.addEventListener('mouseenter', () => {
                isHovered = true;
            });

            this.container.addEventListener('mouseleave', () => {
                isHovered = false;
            });
        }

        // Control táctil
        let isDown = false;
        let startX;
        let scrollLeft;

        this.container.addEventListener('mousedown', (e) => {
            isDown = true;
            isHovered = true;
            this.container.style.cursor = 'grabbing';
            startX = e.pageX - this.container.offsetLeft;
            scrollLeft = this.container.scrollLeft;
        });

        this.container.addEventListener('mouseleave', () => {
            isDown = false;
            isHovered = false;
            this.container.style.cursor = 'grab';
        });

        this.container.addEventListener('mouseup', () => {
            isDown = false;
            setTimeout(() => {
                isHovered = false;
            }, 1000);
            this.container.style.cursor = 'grab';
        });

        this.container.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - this.container.offsetLeft;
            const walk = (x - startX) * 2;
            scrollPos = scrollLeft - walk;
            this.container.scrollLeft = scrollPos;
        });
    }
} 