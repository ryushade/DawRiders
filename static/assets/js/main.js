/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close')

/*===== MENU SHOW =====*/
/* Validate if constant exists */
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu')
    })
}



document.addEventListener('DOMContentLoaded', function () {
    const sliderContainer = document.querySelector('.slider-container');
    const slides = sliderContainer.querySelectorAll('.slider-item');
    let currentIndex = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.display = i === index ? 'block' : 'none';
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    }

    // Iniciar el carrusel mostrando el primer slide
    showSlide(currentIndex);

    // Cambiar slide cada 3 segundos
    setInterval(nextSlide, 3000);
});
/*===== MENU HIDDEN =====*/
/* Validate if constant exists */
if (navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu')
    })
}

/*=============== REMOVE MENU MOBILE ===============*/
const navLink = document.querySelectorAll('.nav__link')

function linkAction() {
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*=============== CHANGE BACKGROUND HEADER ===============*/
function scrollHeader() {
    const header = document.getElementById('header')
    // When the scroll is greater than 50 viewport height, add the scroll-header class to the header tag
    if (this.scrollY >= 50) header.classList.add('scroll-header'); else header.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)




/*=============== POPULAR SWIPER ===============*/
let swiperPopular = new Swiper('.popular__container', {
    loop: true,
    spaceBetween: 24,
    slidesPerView: "auto",
    grabCursor: true,

    pagination: {
        el: ".swiper-pagination",
        dynamicBullets: true,
    },
    breakpoints: {
        768: {
            slidesPerView: 3,
        },
        1024: {
            spaceBetween: 48,
        },
    },
});

/*=============== MIXITUP FILTER FEATURED ===============*/
let mixerFeatured = mixitup('.featured__content', {
    selectors: {
        target: '.featured__card'
    },
    animation: {
        duration: 300
    }
});

/* Link active featured */
const linkFeatured = document.querySelectorAll('.featured__item')

function activeFeatured() {
    linkFeatured.forEach(l => l.classList.remove('active-featured'))
    this.classList.add('active-featured')
}
linkFeatured.forEach(l => l.addEventListener('click', activeFeatured))

/*=============== SHOW SCROLL UP ===============*/
function scrollUp() {
    const scrollUp = document.getElementById('scroll-up');
    // When the scroll is higher than 350 viewport height, add the show-scroll class to the a tag with the scroll-top class
    if (this.scrollY >= 350) scrollUp.classList.add('show-scroll'); else scrollUp.classList.remove('show-scroll')
}
window.addEventListener('scroll', scrollUp)

/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll('section[id]')

function scrollActive() {
    const scrollY = window.pageYOffset

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight,
            sectionTop = current.offsetTop - 58,
            sectionId = current.getAttribute('id')

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.add('active-link')
        } else {
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.remove('active-link')
        }
    })
}
window.addEventListener('scroll', scrollActive)

/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
    origin: 'top',
    distance: '60px',
    duration: 2500,
    delay: 400,
    // reset: true
})

function togglePasswordVisibility() {
    var passwordInput = document.getElementById('contraseña');
    var toggleIcon = document.getElementById('toggle-password-icon');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

function increment() {
    var input = document.getElementById('quantity');
    var currentValue = parseInt(input.value);
    var maxValue = parseInt(input.max);
    if (currentValue < maxValue) {
        input.value = currentValue + 1;
    }
}

function decrement() {
    var input = document.getElementById('quantity');
    var currentValue = parseInt(input.value);
    var minValue = parseInt(input.min);
    if (currentValue > minValue) {
        input.value = currentValue - 1;
    }
}

function decrementItem(idItemCarrito) {
    var quantityInput = document.getElementById('quantity' + idItemCarrito);
    var currentValue = parseInt(quantityInput.value);
    var minValue = parseInt(quantityInput.min);
    if (currentValue > minValue) {
        quantityInput.value = currentValue - 1;
    }
}

function incrementItem(idItemCarrito) {
    var quantityInput = document.getElementById('quantity' + idItemCarrito);
    var currentValue = parseInt(quantityInput.value);
    var maxValue = parseInt(quantityInput.max);
    if (currentValue < maxValue) {
        quantityInput.value = currentValue + 1;
    }
}




sr.reveal(`.home__title, .popular__container, .features__img, .featured__filters`)
sr.reveal(`.home__subtitle`, { delay: 500 })
sr.reveal(`.home__elec`, { delay: 600 })
sr.reveal(`.home__img`, { delay: 800 })
sr.reveal(`.home__car-data`, { delay: 900, interval: 100, origin: 'bottom' })
sr.reveal(`.home__button`, { delay: 1000, origin: 'bottom' })
sr.reveal(`.about__group, .offer__data`, { origin: 'left' })
sr.reveal(`.about__data, .offer__img`, { origin: 'right' })
sr.reveal(`.features__map`, { delay: 600, origin: 'bottom' })
sr.reveal(`.features__card`, { interval: 300 })
sr.reveal(`.featured__card, .logos__content, .footer__content`, { interval: 100 })