document.addEventListener('DOMContentLoaded', function () {


    $('#size').click(function () {

        atr = String($('#size').attr('class'))
        var preview = document.getElementById("id_size"); //getElementById instead of querySelectorAll
        preview.setAttribute("value", atr);
    })

});