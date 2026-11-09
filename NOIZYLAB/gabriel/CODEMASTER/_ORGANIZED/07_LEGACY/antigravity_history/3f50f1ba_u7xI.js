// script.js

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Scroll Progress Bar ---
    const progressBar = document.querySelector('.progress-bar');
    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.body.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        progressBar.style.width = `${scrollPercent}%`;
    });

    // --- Intersection Observer for Eras ---
    // This allows us to detecting which Era is currently in view 
    // and switch the global CSS theme accordingly.
    
    const eras = document.querySelectorAll('.era');
    const body = document.body;

    const observerOptions = {
        root: null,
        rootMargin: '-40% 0px -40% 0px', // Trigger when element is near center of screen
        threshold: 0
    };

    const eraObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const theme = entry.target.getAttribute('data-theme');
                console.log(`Switching theme to: ${theme}`);
                
                // Update body attribute to trigger CSS Variable changes
                body.setAttribute('data-active-theme', theme);
                
                // Animate entry elements
                entry.target.classList.add('in-view');
            }
        });
    }, observerOptions);

    eras.forEach(era => {
        eraObserver.observe(era);
    });
    
    
    // --- Initial Theme Set ---
    // If loaded at top, dragging scrollbar, etc. ensure first theme applies.
    if (window.scrollY < 100) {
        body.setAttribute('data-active-theme', 'origins');
    }
});
