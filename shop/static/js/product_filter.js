document.addEventListener('DOMContentLoaded', function () {

    let brand = []
    let size = []
    let category = []
    let subcategory_type = []
    let subcategory = []

    $(".category").click(function () {
        var category_type = $(this).data('id')
        category = []
        category.push(category_type)
        getProductByFilter(category, subcategory, subcategory_type, brand, size)
    });

    $('.subcategory').click(function () {
        var subcategory_types = $(this).data('id')
        subcategory = []
        subcategory.push(subcategory_types)
        getProductByFilter(category, subcategory, subcategory_type, brand, size)
    });

    $('.subcategory_type_type_t').click(function () {
        var subcategory_type_t = $(this).data('id')
        subcategory_type = []
        subcategory_type.push(subcategory_type_t)
        getProductByFilter(category, subcategory, subcategory_type, brand, size)
    })
    $('.brands').click(function () {
        var brand_type = $(this).data('id')
        brand = []
        brand.push(brand_type)
        getProductByFilter(category, subcategory, subcategory_type, brand, size)
    })
    $('.size').click(function () {
        var size_type = $(this).data('id')
        size = []
        size.push(size_type)
        getProductByFilter(category, subcategory, subcategory_type, brand, size)
    })


    $(".clear_filter").click(function () {
        location.reload()
    })


    function updateFilters() {

        if (document.getElementsByClassName('category').length > 1) {
            for (var i = 0; i < document.getElementsByClassName('category').length; i++) {
                category.push(document.getElementsByClassName('category')[i].getAttribute('data-id'))
            }
        } else {
            category.push(document.getElementsByClassName('category')[0].getAttribute('data-id'))
        }

        if (document.getElementsByClassName('subcategory').length > 1) {
            for (var b = 0; b < document.getElementsByClassName('subcategory').length; b++) {
                subcategory.push(document.getElementsByClassName('subcategory')[b].getAttribute('data-id'))
            }
        } else {
            subcategory.push(document.getElementsByClassName('subcategory')[0].getAttribute('data-id'))
        }

        if (document.getElementsByClassName('subcategory_type_type_t').length > 1) {
            for (var c = 0; c < document.getElementsByClassName('subcategory_type_type_t').length; c++) {
                subcategory_type.push(document.getElementsByClassName('subcategory_type_type_t')[c].getAttribute('data-id'))
            }
        } else {
            subcategory_type.push(document.getElementsByClassName('subcategory_type_type_t')[0].getAttribute('data-id'))
        }

        if (document.getElementsByClassName('brands').length > 1) {
            for (var d = 0; d < document.getElementsByClassName('brands').length; d++) {
                brand.push(document.getElementsByClassName('brands')[d].getAttribute('data-id'))
            }
        } else {
            brand.push(document.getElementsByClassName('brands')[0].getAttribute('data-id'))
        }

       if (document.getElementsByClassName('size').length > 1) {
            for (var e = 0; e < document.getElementsByClassName('size').length; e++) {
                size.push(document.getElementsByClassName('size')[e].getAttribute('data-id'))
            }
        } else {
            size.push(document.getElementsByClassName('size')[0].getAttribute('data-id'))
        }

    }
    updateFilters()
    console.log(category, subcategory, subcategory_type, brand, size)
});


function getProductByFilter(category, subcategory, subcategory_type, brand, size) {
    console.log(category, subcategory, subcategory_type, brand, size)
    $.ajax({
        data: {
            'category': category,
            'subcategory': subcategory,
            'subcategorytype': subcategory_type,
            'brand': brand,
            'size': size
        },
        url: "/json-filter/",
        success: function (response) {
            render(response['render'])
            if ($('.clear_all ').attr('class') == 'clear_all clear_all_active') {

            } else {
                $('.clear_all').toggleClass('clear_all_active')
            }
        },
        error: function (response) {
            console.log(response.responseJSON.errors)
        }
    });
}

function render(rendered) {
    $('.products-list').remove()
    $('.paginator-list').remove()
    $('.product-list').append(rendered)
}