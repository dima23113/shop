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
                console.log(textinp.value)
                if (sign === '+') {
                    tmp = Number(textinp.value) + 1
                    textinp.setAttribute('value', tmp)
                    textinp.setAttribute('data-qty', tmp)
                    console.log(textinp)
                } else {
                    if (textinp.value === '0') {
                    } else {
                        tmp = Number(textinp.value) - 1
                        textinp.setAttribute('value', tmp)
                        textinp.setAttribute('data-qty', tmp)
                    }
                }

            }
        )
    })

    function maxQty() {
        a = document.getElementsByClassName('')
    }

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



