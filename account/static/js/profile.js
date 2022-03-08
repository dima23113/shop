function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {


    $('.phone').click(function () {
        if ($('.phone-form').attr('class') == 'phone-form form_active') {
            $('.phone-form').removeClass('form_active');
        } else {
            closeForm()
            $('.phone-form').addClass('form_active');
        }
    })

    $('.bio').click(function () {
        if ($('.bio-form').attr('class') == 'bio-form form_active') {
            $('.bio-form').removeClass('form_active');
        } else {
            closeForm()
            $('.bio-form').addClass('form_active');
        }
    })

    $('.password').click(function () {
        if ($('.password-change-form').attr('class') == 'password-change-form form_active') {
            $('.password-change-form').removeClass('form_active');
        } else {
            closeForm()
            $('.password-change-form').addClass('form_active');
        }
    })

    $('.mailing').click(function () {
        if ($('.mailing-form').attr('class') == 'mailing-form form_active') {
            $('.mailing-form').removeClass('form_active');
        } else {
            closeForm()
            $('.mailing-form').addClass('form_active');
        }
    })

    $('.email').click(function () {
        if ($('.email-form').attr('class') == 'email-form form_active') {
            $('.email-form').removeClass('form_active');
        } else {
            closeForm()
            $('.email-form').addClass('form_active');
        }
    })

    function closeForm() {
        $('.phone-form').removeClass('form_active');
        $('.bio-form').removeClass('form_active');
        $('.password-change-form').removeClass('form_active');
        $('.mailing-form').removeClass('form_active');
        $('.email-form').removeClass('form_active');
    }

    $(document).ready(function () {
        $(".remove_link").click(function () {
            var product = $(this).data('id')
            $.ajax({
                data: {'product': product, 'csrfmiddlewaretoken': csrftoken},
                url: 'http://127.0.0.1:8000/favorites/remove/' + product + '/',
                method: 'post',
                success: function (response) {
                    $('#' + product).remove()
                },
                error: function (response) {
                    console.log(response)
                }
            })

        });
    });
})
;