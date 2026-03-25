// core logic

document.addEventListener('DOMContentLoaded', () => {
    // 1. Navbar Scroll Effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 20) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.add('scrolled'); // keep dark for now or toggle
                if (window.scrollY < 20) {
                    navbar.classList.remove('scrolled');
                }
            }
        });
    }

    // 2. Check Auth Status (Simulation)
    const token = localStorage.getItem('access_token');
    const authContainer = document.getElementById('nav-auth-container');
    const userMenu = document.getElementById('nav-user-menu');

    if (token) {
        if (authContainer) authContainer.style.display = 'none';
        if (userMenu) userMenu.style.display = 'flex';
    } else {
        if (authContainer) authContainer.style.display = 'flex';
        if (userMenu) userMenu.style.display = 'none';
    }
});

// Logout function
window.logout = function () {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/';
};
