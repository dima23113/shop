document.addEventListener('DOMContentLoaded', function () {

    $(document).ready(function () {
        $(".size").click(function () {
            var buttonData = $(this).data("mydata");
            var preview = document.getElementById("id_size"); //getElementById instead of querySelectorAll
            preview.setAttribute("value", buttonData);
        });
    });
});


