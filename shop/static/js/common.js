document.addEventListener('DOMContentLoaded', function () {
    function toggleMenu() {
        $('.menu-toggle').toggleClass('menu-toggle_active');
        $('.left-menu').toggleClass('left-menu_active');
        $('.right-auth').toggleClass('right-auth_active');
        $('.navbar').toggleClass('navbar_active');

    }

    $('.menu-toggle').click(function () {
        toggleMenu();
    })

    function closeMenu() {
        $('.menu-toggle').removeClass('menu-toggle_active');
        $('.left-menu').removeClass('left-menu_active');
        $('.right-auth').removeClass('right-auth_active');
        $('.navbar').removeClass('navbar_active');
    }


    $(document).click(function (e) {
        if ($(e.target).closest('.menu-container').length) return;
        closeMenu();

    })

});

$('document').ready(function () {
    screenClass();
    $(window).resize(function () {
        screenClass();
    });

    function closeMenu() {
        $('.menu-toggle').removeClass('menu-toggle_active');
        $('.left-menu').removeClass('left-menu_active');
        $('.right-auth').removeClass('right-auth_active');
        $('.navbar').removeClass('navbar_active');
    }

    function screenClass() {
        if ($(window).innerWidth() > 1027) {
            closeMenu()
        } else {
        }
    }
})