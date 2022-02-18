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
        $('#menu_phone').toggleClass('menu_phone_active')
        $('.navbar').toggleClass('navbar_active');
    }

    $('.search').click(function () {
        if ($('.search-form').attr('class') == 'search-form search-form__active') {
            $('.search-form').removeClass('search-form__active')
            $('.cart').css('margin-top', '14px')
        } else {
            $('.search-form').toggleClass('search-form__active')
            $('.cart').css('margin-top', '74px')
            window.scrollTo(0, 100)
            console.log($('.search-form').attr('class'))
        }
    })

    $('.sort_by').click(function () {
        if ($('.sort_toggle_d').attr('class') == 'sort_toggle_d sort_toggle_d_active') {
            $('.sort_toggle_d').removeClass('sort_toggle_d_active')
        } else {
            $('.sort_toggle_d').toggleClass('sort_toggle_d_active')
        }
    })

    $('.filter_toggle').click(function () {
        if ($('.filter_toggle_d').attr('class') == 'filter_toggle_d filter_toggle_d_active') {
            $('.filter_toggle_d').removeClass('filter_toggle_d_active')
        } else {
            $('.filter_toggle_d').toggleClass('filter_toggle_d_active')
        }
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


var indexSwiper = new Swiper(".indexSwiper", {
        spaceBetween: 30,
        centeredSlides: true,
        autoplay: {
          delay: 3000,
          disableOnInteraction: false,
        },
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      });