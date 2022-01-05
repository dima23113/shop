document.addEventListener('DOMContentLoaded', function () {
    function toggleMenu() {
        $('.menu-toggle').toggleClass('menu-toggle_active')
        $('.left-menu').toggleClass('left-menu_active')
        $('.right-auth').toggleClass('right-auth_active')
    }

    $('.menu-toggle').click(function () {
        toggleMenu()
    })

    function closeMenu(){
        $('.menu-toggle').removeClass('menu-toggle_active')
        $('.left-menu').removeClass('left-menu_active')
        $('.right-auth').removeClass('right-auth_active')
    }
    $(document).click(function (e) {
        if ($(e.target).closest('.menu-container').length) return
        closeMenu()
    })
})

