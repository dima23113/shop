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
            success: function (response) {
                console.log(response['price'])
                c = ['Стоимость товаров: ', 'Стоимость товаров со скидкой: ', 'Итого: ']
                r = document.getElementsByClassName('price_')
                for (var i = 0; i < r.length; i++) {
                    r[i].innerHTML = c[i] + response['price']
                }
            }
        })
    }, 100)
}


function updateQtyCart() {
    setTimeout(function () {
        $.ajax({
            url: 'cart-qty/',
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
            console.log(product_id)
            $.ajax({
                data: {'product_id': product_id, 'csrfmiddlewaretoken': csrftoken},
                url: "remove/",
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
                var textinp = document.getElementsByClassName(product)[0]
                var id = $(this).data('id')
                console.log(textinp.value)
                if (sign === '+') {
                    if (Number(textinp.getAttribute('data-max_qty')) > textinp.value) {
                        tmp = Number(textinp.value) + 1
                        textinp.setAttribute('value', tmp)
                        textinp.setAttribute('data-qty', tmp)
                        console.log(textinp)
                        updateQty(id, tmp, textinp.getAttribute('data-max_qty'))
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
                        updateQty(id, tmp, textinp.getAttribute('data-max_qty'))
                        updatePrice()
                        updateQtyCart()
                    }
                }
            }
        )
    })

    function updateQty(product, qty, max_qty) {
        $.ajax({
            data: {'product': product, 'qty': qty, 'max_qty': max_qty, 'csrfmiddlewaretoken': csrftoken},
            url: 'qty/',
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

function setInputFilter(textbox, inputFilter) {
    ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function (event) {
        textbox.addEventListener(event, function () {
            if (inputFilter(this.value)) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            } else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            } else {
                this.value = "";
            }
        });
    });
}

setInputFilter(document.getElementById("intLimitTextBox"), function (value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 50);
});



