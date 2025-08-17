// Theme Toggle Functionality - Optimized for performance
document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;

    // Batch DOM reads to avoid forced reflows
    const savedTheme = localStorage.getItem('theme') || 'light';
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const systemTheme = prefersDark ? 'dark' : 'light';
    const initialTheme = !localStorage.getItem('theme') ? systemTheme : savedTheme;

    // Single DOM write operation
    html.setAttribute('data-theme', initialTheme);
    if (!localStorage.getItem('theme')) {
        localStorage.setItem('theme', systemTheme);
    }

    // Theme toggle click handler - optimized to reduce reflows
    themeToggle.addEventListener('click', function () {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';

        // Batch DOM operations using requestAnimationFrame
        requestAnimationFrame(() => {
            // Update theme and localStorage in one frame
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);

            // Add button animation
            themeToggle.style.transform = 'scale(0.95)';
            setTimeout(() => {
                themeToggle.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Listen for system theme changes - optimized
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', function (e) {
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            requestAnimationFrame(() => {
                html.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
            });
        }
    });
});

// Optimized theme transitions - add CSS once instead of inline styles
function addThemeTransition() {
    // Check if style already exists to avoid duplicates
    if (!document.getElementById('theme-transitions')) {
        const style = document.createElement('style');
        style.id = 'theme-transitions';
        style.textContent = `
            * {
                transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize theme transitions
addThemeTransition();
