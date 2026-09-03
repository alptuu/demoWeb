(function () {
    'use strict';

    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* Mobile navigation ------------------------------------------------- */

    var toggle = document.querySelector('[data-nav-toggle]');
    var nav = document.querySelector('[data-nav]');

    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            var open = document.body.classList.toggle('nav-open');
            toggle.setAttribute('aria-expanded', String(open));
        });

        nav.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                document.body.classList.remove('nav-open');
                toggle.setAttribute('aria-expanded', 'false');
            });
        });
    }

    /* Nav background on scroll ------------------------------------------ */

    var siteNav = document.querySelector('.site-nav');

    /* Scroll progress rail ---------------------------------------------- */

    var progressBar = document.querySelector('[data-scroll-progress]');
    var scrollTopBtn = document.querySelector('[data-scroll-top]');

    function onScroll() {
        var scrolled = window.scrollY;

        if (siteNav) {
            siteNav.classList.toggle('is-scrolled', scrolled > 40);
        }

        if (scrollTopBtn) {
            scrollTopBtn.classList.toggle('is-visible', scrolled > 400);
        }

        if (progressBar) {
            var max = document.documentElement.scrollHeight - window.innerHeight;
            var ratio = max > 0 ? Math.min(scrolled / max, 1) : 0;
            progressBar.style.height = (ratio * 100) + '%';
        }
    }

    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', function () {
            window.scrollTo({
                top: 0,
                behavior: prefersReducedMotion ? 'auto' : 'smooth'
            });
        });
    }

    var ticking = false;

    window.addEventListener('scroll', function () {
        if (!ticking) {
            window.requestAnimationFrame(function () {
                onScroll();
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });

    onScroll();

    /* Reveal on scroll --------------------------------------------------- */

    var revealItems = document.querySelectorAll('.reveal');

    if (prefersReducedMotion || !('IntersectionObserver' in window)) {
        revealItems.forEach(function (item) {
            item.classList.add('is-visible');
        });
    } else {
        var revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

        revealItems.forEach(function (item) {
            revealObserver.observe(item);
        });
    }

    /* Scrollspy ---------------------------------------------------------- */

    var sections = document.querySelectorAll('[data-section]');
    var navLinks = document.querySelectorAll('[data-nav-link]');

    if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
        var spyObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) {
                    return;
                }

                navLinks.forEach(function (link) {
                    var isActive = link.getAttribute('href').endsWith('#' + entry.target.id);
                    link.classList.toggle('is-active', isActive);
                });
            });
        }, { threshold: 0.15, rootMargin: '-40% 0px -50% 0px' });

        sections.forEach(function (section) {
            spyObserver.observe(section);
        });
    }

    /* Animated counters --------------------------------------------------- */

    var counters = document.querySelectorAll('[data-counter]');

    function runCounter(el) {
        var target = parseInt(el.getAttribute('data-counter'), 10) || 0;
        var suffix = el.getAttribute('data-suffix') || '';

        if (prefersReducedMotion) {
            el.textContent = target + suffix;
            return;
        }

        var duration = 1400;
        var start = null;

        function step(timestamp) {
            if (start === null) {
                start = timestamp;
            }

            var progress = Math.min((timestamp - start) / duration, 1);
            el.textContent = Math.floor(progress * target) + suffix;

            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        }

        window.requestAnimationFrame(step);
    }

    if (counters.length && 'IntersectionObserver' in window) {
        var counterObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    runCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(function (counter) {
            counterObserver.observe(counter);
        });
    } else {
        counters.forEach(runCounter);
    }

    /* Testimonial carousel ------------------------------------------------ */

    var carousel = document.querySelector('[data-carousel]');

    if (carousel) {
        var slides = carousel.querySelectorAll('[data-carousel-slide]');
        var dots = carousel.querySelectorAll('[data-carousel-dot]');
        var index = 0;
        var timer = null;

        function show(next) {
            index = (next + slides.length) % slides.length;

            slides.forEach(function (slide, i) {
                slide.classList.toggle('is-active', i === index);
            });

            dots.forEach(function (dot, i) {
                dot.classList.toggle('is-active', i === index);
                dot.setAttribute('aria-selected', String(i === index));
            });
        }

        function play() {
            if (slides.length < 2 || prefersReducedMotion) {
                return;
            }

            stop();
            timer = window.setInterval(function () {
                show(index + 1);
            }, 6000);
        }

        function stop() {
            if (timer !== null) {
                window.clearInterval(timer);
                timer = null;
            }
        }

        dots.forEach(function (dot, i) {
            dot.addEventListener('click', function () {
                show(i);
                play();
            });
        });

        carousel.addEventListener('mouseenter', stop);
        carousel.addEventListener('mouseleave', play);

        show(0);
        play();
    }

    /* Custom cursor ------------------------------------------------------- */

    var cursor = document.querySelector('[data-cursor]');
    var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    if (cursor && finePointer && !prefersReducedMotion) {
        var cursorX = 0;
        var cursorY = 0;
        var cursorTicking = false;

        document.addEventListener('mousemove', function (event) {
            cursorX = event.clientX;
            cursorY = event.clientY;
            document.body.classList.add('has-cursor');

            if (!cursorTicking) {
                window.requestAnimationFrame(function () {
                    cursor.style.setProperty('--cursor-x', cursorX + 'px');
                    cursor.style.setProperty('--cursor-y', cursorY + 'px');
                    cursorTicking = false;
                });
                cursorTicking = true;
            }
        });

        document.addEventListener('mouseover', function (event) {
            var interactive = event.target.closest('a, button, [role="tab"], input, textarea');
            cursor.classList.toggle('is-active', Boolean(interactive));
        });

        document.addEventListener('mouseleave', function () {
            document.body.classList.remove('has-cursor');
        });
    }
})();
