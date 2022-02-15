from .models import *


def sort_brand_list_into_2_columns():
    """Создаем список для сортировки брендов по алфавиту и группировки их по первой букве. Делим список на 2 для
    вывода списка брендов в 2 колонки """
    lst = []
    brand = Brand.objects.all()
    for i in brand:
        s = {
            'symbol': i.name[0].upper(),
            'name': i.name,
            'slug': i.slug
        }
        lst.append(s)
    lst1 = lst[(len(lst) // 2) + 1:]
    lst = lst[:(len(lst) // 2) + 1]
    context = {
        'brand_cl': lst,
        'brand_cl_1': lst1
    }
    return context


def get_product_list_by(category=None, brand=None, subcategory=None, subcategory_type=None):
    """Выдаем товары и submenu для выбранной категории/подкатегории/типа подкатегории"""
    if category:
        products = Product.objects.filter(category__slug=category,
                                          available=True).select_related(
            'brand').only('image', 'slug', 'brand', 'name', 'price', 'id')
        category, subcategory, subcategory_type, sizes, brands = get_left_filter_submenu(products)
        return category, sizes, products, subcategory, subcategory_type, brands
    if brand:
        products = Product.objects.filter(brand__slug=brand, available=True)
        category, subcategory, subcategory_type, sizes, brand = get_left_filter_submenu(products)
        return brand, products, category, subcategory, subcategory_type, sizes

    if subcategory:
        products = Product.objects.filter(
            subcategory__slug=subcategory,
            available=True).only('image', 'slug', 'brand', 'name', 'price', 'id')
        category, subcategory, subcategory_type, sizes, brands = get_left_filter_submenu(products)
        return subcategory, products, category, subcategory_type, brands, sizes

    if subcategory_type:
        products = Product.objects.filter(subcategory_type__slug=subcategory_type,
                                          available=True).only('image', 'slug', 'brand', 'name', 'price', 'id')
        category, subcategory, subcategory_type, sizes, brands = get_left_filter_submenu(products)
        return subcategory_type, products, category, subcategory, sizes, brands


def get_left_filter_submenu(product):
    """Получаем submenu для набора товаров"""
    category = Category.objects.filter(products__in=product).distinct('name').only('id', 'slug', 'name')
    subcategory = Subcategory.objects.filter(subcategory_products__in=product).distinct().only('id', 'slug', 'name')
    subcategory_type = SubcategoryType.objects.filter(subcategory_type_products__in=product). \
        distinct('name').only('id', 'slug', 'name')
    sizes = ProductSize.objects.filter(product__in=product).distinct('name').only('id', 'name')
    brands = Brand.objects.filter(product__in=product).distinct('name')
    return category, subcategory, subcategory_type, sizes, brands
