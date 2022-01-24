document.addEventListener('DOMContentLoaded', function () {

    $(document).ready(function () {
        $(".sizes").click(function () {
            var Size = $(this).data("mydata");
            var id = $(this).data('id');
            console.log(Size)
            console.log(id)

            $.ajax({
                data: [Size, id],
                url: "{% url 'check_qty' %}",
                success: function (response) {
                    console.log(response)
                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }

            })

            //var preview = document.getElementById("id_size"); //getElementById instead of querySelectorAll
            //preview.setAttribute("value", buttonData);
        });
    });
});


