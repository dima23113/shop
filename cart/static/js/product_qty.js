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

function updatePrice() {
    setTimeout(function () {
        $.ajax({
            url: 'price/',
            headers: {'Access-Control-Allow-Origin': '*'},
            success: function (response) {
                c = ['Стоимость товаров: ', 'Стоимость товаров со скидкой: ', 'Итого: ']
                c1 = []
                c1.push('Стоимость товаров: ' + response['price'])
                c1.push('Стоимость товаров со скидкой: ' + response['price_discount'])
                c1.push('Стоимость товаров: ' + response['price_discount'])
                r = document.getElementsByClassName('price_')
                for (var i = 0; i < r.length; i++) {
                    r[i].innerHTML = c1[i]
                }
            }
        })
    }, 100)
}


function updateQtyCart() {
    setTimeout(function () {
        $.ajax({
            url: 'cart-qty/',
            headers: {'Access-Control-Allow-Origin': '*'},
            success: function (response) {
                console.log(response['cart_qty'])
                r = document.getElementById('cart_qty')
                r.textContent = '[' + response['cart_qty'] + ']'
            }
        })
    }, 200)
}

const csrftoken = getCookie('csrftoken');


document.addEventListener('DOMContentLoaded', function () {
    $(document).ready(function () {
        $(".remove-btn").click(function () {
            var product_id = $(this).data('product')
            var size = $(this).data('size')
            product_id = product_id + '-' + size
            console.log(product_id)
            $.ajax({
                data: {'product_id': product_id, 'csrfmiddlewaretoken': csrftoken},
                url: "remove/",
                headers: {'Access-Control-Allow-Origin': '*'},
                method: 'post',
                success: function (response) {
                    var els = document.getElementById(response['id'])
                    els.parentNode.parentNode.removeChild(els.parentNode);
                    updateQtyCart()
                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }
            });

        });
    });
    $(document).ready(function () {
        $(".sign").click(function () {
                var product = $(this).data('name')
                var sign = $(this).html()
                var id = $(this).data('id')
                tmp = 'intLimitTextBox' + id
                var textinp = document.getElementById(tmp)
                var size = textinp.getAttribute('data-size')
                console.log(textinp)
                console.log(textinp.value)
                if (sign === '+') {
                    if (Number(textinp.getAttribute('data-max_qty')) > textinp.value) {
                        tmp = Number(textinp.value) + 1
                        textinp.setAttribute('value', tmp)
                        textinp.setAttribute('data-qty', tmp)
                        console.log(textinp)
                        updateQty(id, tmp, textinp.getAttribute('data-max_qty'), size)
                        updatePrice()
                        updateQtyCart()
                    } else {
                        console.log('Превышен лимит товара')
                        console.log(Number(textinp.getAttribute('data-max_qty')))
                    }

                } else {
                    if (textinp.value === '1') {
                    } else {
                        tmp = Number(textinp.value) - 1
                        textinp.setAttribute('value', tmp)
                        textinp.setAttribute('data-qty', tmp)
                        updateQty(id, tmp, textinp.getAttribute('data-max_qty'), size)
                        updatePrice()
                        updateQtyCart()
                    }
                }
            }
        )
    })

    function updateQty(product, qty, max_qty, size) {
        $.ajax({
            data: {'product': product, 'qty': qty, 'max_qty': max_qty, 'size': size, 'csrfmiddlewaretoken': csrftoken},
            url: 'qty/',
            headers: {'Access-Control-Allow-Origin': '*'},
            method: 'post',
            success: function (response) {
                console.log(response)
            },
            error: function (response) {
                console.log(response)
            }
        })
    }

    $(document).ready(function () {
        $(".remove-all").click(function () {
            $.ajax({
                data: {'remove_all': true, 'csrfmiddlewaretoken': csrftoken},
                url: "remove/",
                headers: {'Access-Control-Allow-Origin': '*'},
                method: 'post',
                success: function (response) {
                    console.log(response)
                    var els = document.getElementsByClassName('items-wrapper')[0]
                    els.remove()
                    updateQtyCart()
                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }
            });
        });
    });

    function maxQty() {
        a = document.getElementsByName('product-qty')
        a.forEach(a => {
                var product = a.className
                var size = a.getAttribute('data-size')
                $.ajax({
                    data: {'product': product, 'size': size},
                    headers: {'Access-Control-Allow-Origin': '*'},
                    url: 'qty/',
                    success: function (response) {
                        console.log(response)
                        product_ = response['product']
                        maxqty = response['max_qty']
                        a.setAttribute('data-max_qty', maxqty)
                    },
                    error: function (response) {
                        console.log(response)
                    }
                })
            }
        )
    }

    maxQty()

});




