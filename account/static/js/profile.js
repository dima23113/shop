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

    function closeForm() {
        $('.phone-form').removeClass('form_active');
        $('.bio-form').removeClass('form_active');
        $('.password-change-form').removeClass('form_active');
        $('.mailing-form').removeClass('form_active');
    }

});