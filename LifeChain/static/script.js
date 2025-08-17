// Ensure jQuery is loaded before running this code
(function () {
    function initScript() {
        if (typeof jQuery !== 'undefined' && typeof $ !== 'undefined') {
            $(document).ready(function () {
                // Cache DOM elements to avoid repeated queries
                const $bars = $('.fa-bars');
                const $navbar = $('.navbar');
                const $header = $('header');
                let ticking = false;
                let lastScrollTop = 0;

                // Mobile menu toggle
                $bars.click(function () {
                    $(this).toggleClass('fa-times');
                    $navbar.toggleClass('nav-toggle');
                });

                // Optimized scroll effects with throttling
                function updateScrollEffects() {
                    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

                    // Only update if scroll position changed significantly
                    if (Math.abs(scrollTop - lastScrollTop) > 5) {
                        $bars.removeClass('fa-times');
                        $navbar.removeClass('nav-toggle');

                        if (scrollTop > 30) {
                            $header.addClass('header-active');
                        } else {
                            $header.removeClass('header-active');
                        }

                        lastScrollTop = scrollTop;
                    }
                    ticking = false;
                }

                // Throttle scroll events to reduce reflows
                function requestScrollUpdate() {
                    if (!ticking) {
                        requestAnimationFrame(updateScrollEffects);
                        ticking = true;
                    }
                }

                // Use passive scroll listener for better performance
                $(window).on('scroll', requestScrollUpdate, { passive: true });

                // Initial call for load event
                updateScrollEffects();
            });
        } else {
            // Retry after a short delay if jQuery isn't ready yet
            setTimeout(initScript, 100);
        }
    }

    // Start initialization
    initScript();
})();