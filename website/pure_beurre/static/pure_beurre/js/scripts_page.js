var nav = document.querySelector("#mainNav");

window.addEventListener('scroll', () => {
     if (window.scrollY < 200 ) {
         nav.classList.add("navbar-scrolled");
     } else {
        nav.classList.remove("navbar-scrolled");
        }
});
