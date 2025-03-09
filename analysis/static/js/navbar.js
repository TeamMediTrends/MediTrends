document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const navLinks = document.getElementById("nav-links");

    console.log(menuToggle, navLinks);  // Debugging log to check elements are found

    menuToggle.addEventListener("click", function () {
        navLinks.classList.toggle("active");
    });
});