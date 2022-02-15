$('#products-menu').clone(true).unwrap().appendTo('#menu_phone');
a = document.getElementsByClassName('menu-toggle')[0]
$('#menu_phone')[0].getElementsByClassName('products')[0].getElementsByClassName('menu-toggle')[0].remove()
$('#products-menu-right').clone(true).unwrap().appendTo('#menu_phone')
$('#menu_phone')[0].getElementsByClassName('products')[0].setAttribute('class', 'menu_phone_left')
$('#menu_phone')[0].getElementsByClassName('auth')[0].setAttribute('class', 'menu_phone_right')
$('#menu_phone')[0].getElementsByClassName('menu_phone_right')[0].getElementsByClassName('right-auth')[0].setAttribute('class', 'menu_phone_right_ul')
$('#menu_phone')[0].getElementsByClassName('menu_phone_left')[0].getElementsByClassName('left-menu')[0].setAttribute('class', 'menu_phone_left_ul')
document.addEventListener('DOMContentLoaded', function () {
    function toggleMenu() {
        $('.menu-toggle').toggleClass('menu-toggle_active');
        //$('.left-menu').toggleClass('left-menu_active');
        //$('.right-auth').toggleClass('right-auth_active');
        $('#menu_phone').toggleClass('menu_phone_active')
        //$('#menu_phone').getElementsByClassName('products')[0].toggleClass('left-menu_active')
        $('.navbar').toggleClass('navbar_active');


    }

    $('.search').click(function () {
        $('.search-form').toggleClass('search-form__active')
        window.scrollTo(0, 100)
    })

    $('.menu-toggle').click(function () {
        toggleMenu();
    })

    $('.detail').click(function () {
        $('.info-a').removeClass('info-a_active');
        $('.ship-a').removeClass('ship-a_active');
        $('.ship').removeClass('ship_active');
        $('.detail').removeClass('detail_none');
    })


    $('.ship').click(function () {
        if ($('.ship-a').attr('class') == 'ship-a ship-a_active') {

        } else {
            $('.ship-a').toggleClass('ship-a_active');
            $('.info-a').toggleClass('info-a_active');
            $('.ship').toggleClass('ship_active');
            $('.detail').toggleClass('detail_none');
        }
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
        //$('.left-menu').removeClass('left-menu_active');
        //$('.right-auth').removeClass('right-auth_active');
        $('#menu_phone').removeClass('menu_phone_active')
        $('.navbar').removeClass('navbar_active');

    }

    function screenClass() {
        if ($(window).innerWidth() > 1027) {
            closeMenu()
        } else {
        }
    }
})


window.onscroll = function () {
    myFunction()
};

var navbar = document.getElementById("navbar");
var sticky = navbar.offsetTop;

function myFunction() {
    if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky")
    } else {
        navbar.classList.remove("sticky");
    }
}


var swiper = new Swiper(".mySwiper", {
    slidesPerView: 1,
    spaceBetween: 30,
    loop: true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});

