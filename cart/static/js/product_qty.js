document.addEventListener('DOMContentLoaded', function () {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $(document).ready(function () {
        $(".sizes").click(function () {
            var Size = $(this).data("mydata");
            var id = $(this).data('id');
            var sign = $(this).html()
            var product_name = $(this).data('class_pr')
            var product_name_cl = document.getElementsByClassName(product_name)[0].getAttribute('value')
            console.log(Size)
            console.log(id)
            $.ajax({
                data: {'product_id': id, 'size': Size},
                url: "{% url 'cart:check_qty' %}",
                success: function (response) {
                    console.log(response)
                    var max_qty = response['qty']
                    var class_name = response['product_name']
                    var product = document.getElementsByClassName(class_name)[0]
                    product.setAttribute('data-max', max_qty)
                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }

            });
            var max_qty = document.getElementsByClassName(product_name)[0].getAttribute('data-max')
            console.log(max_qty)
            $.ajax({
                data: {
                    'product_id': id,
                    'size': Size,
                    'sign': sign,
                    'qty_now': product_name_cl,
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    'max_qty': max_qty
                },
                url: "{% url 'cart:check_qty' %}",
                method: 'post',
                success: function (response) {
                    console.log(response)
                    var product = document.getElementsByClassName(product_name)[0]
                    product.setAttribute('value', response['qty_now'])

                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }

            });

        });
    });
});
