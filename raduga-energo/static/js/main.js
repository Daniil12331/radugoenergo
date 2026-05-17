// ============================================
//  РАДУГА ЭНЕРГО — ПРЕМИАЛЬНЫЙ JS
// ============================================

// === ЧАСТИЦЫ НА ФОНЕ (Canvas) ===
class ParticleSystem {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.mouseX = 0;
        this.mouseY = 0;
        this.init();
    }

    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX;
            this.mouseY = e.clientY;
        });
        this.createParticles();
        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        const count = Math.min(Math.floor(window.innerWidth * 0.06), 80);
        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2 + 0.5,
                alpha: Math.random() * 0.4 + 0.1,
                alphaSpeed: Math.random() * 0.005 + 0.002,
                alphaDir: 1
            });
        }
    }

    animate() {
        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Обновляем и рисуем частицы
        this.particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;

            p.alpha += p.alphaSpeed * p.alphaDir;
            if (p.alpha > 0.5 || p.alpha < 0.05) p.alphaDir *= -1;

            // Циклические границы
            if (p.x < 0) p.x = this.canvas.width;
            if (p.x > this.canvas.width) p.x = 0;
            if (p.y < 0) p.y = this.canvas.height;
            if (p.y > this.canvas.height) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(13, 110, 253, ${p.alpha})`;
            ctx.fill();

            // Свечение
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius * 3, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(13, 110, 253, ${p.alpha * 0.1})`;
            ctx.fill();
        });

        // Линии между ближайшими частицами
        this.drawLines();

        // Реакция на мышь
        this.drawMouseGlow();

        requestAnimationFrame(() => this.animate());
    }

    drawLines() {
        const ctx = this.ctx;
        const maxDist = 120;

        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < maxDist) {
                    const alpha = (1 - dist / maxDist) * 0.15;
                    ctx.beginPath();
                    ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    ctx.strokeStyle = `rgba(13, 110, 253, ${alpha})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
    }

    drawMouseGlow() {
        const ctx = this.ctx;
        const gradient = ctx.createRadialGradient(
            this.mouseX, this.mouseY, 0,
            this.mouseX, this.mouseY, 200
        );
        gradient.addColorStop(0, 'rgba(13, 110, 253, 0.03)');
        gradient.addColorStop(0.5, 'rgba(13, 110, 253, 0.01)');
        gradient.addColorStop(1, 'rgba(13, 110, 253, 0)');

        ctx.beginPath();
        ctx.arc(this.mouseX, this.mouseY, 200, 0, Math.PI * 2);
        ctx.fillStyle = gradient;
        ctx.fill();
    }
}

// === ЭФФЕКТ НАВБАРА ПРИ СКРОЛЛЕ ===
function initNavbarScroll() {
    const navbar = document.getElementById('mainNavbar');
    if (!navbar) return;

    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;

        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Скрываем/показываем при скролле вниз/вверх
        if (currentScroll > lastScroll && currentScroll > 200) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }

        lastScroll = currentScroll;
    });
}

// === ПЛАВНЫЙ СКРОЛЛ ДЛЯ ЯКОРЕЙ ===
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// === ЗАПУСК ПРИ ЗАГРУЗКЕ ===
document.addEventListener('DOMContentLoaded', () => {
    // Частицы
    const particles = new ParticleSystem('particles-canvas');

    // Навбар
    initNavbarScroll();

    // Плавный скролл
    initSmoothScroll();

    // Добавляем класс loaded после полной загрузки
    document.body.classList.add('loaded');
});