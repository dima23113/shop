document.addEventListener('DOMContentLoaded', function () {


    $('#size').click(function () {
        if ($('#size').attr('class') == 'phone-form form_active') {
            $('.phone-form').removeClass('form_active');
        } else {
            closeForm()
            $('.phone-form').addClass('form_active');
        }
    })

    function closeForm() {
        $('.phone-form').removeClass('form_active');
        $('.bio-form').removeClass('form_active');
        $('.password-change-form').removeClass('form_active');
        $('.mailing-form').removeClass('form_active');
        $('.email-form').removeClass('form_active');
    }

});