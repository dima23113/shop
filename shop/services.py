import datetime

from .models import *
from blog.models import Article


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


def get_product_list(obj, slug):
    """Выдаем товары и submenu для выбранной категории/подкатегории/типа подкатегории"""
    if obj == 'category':
        products = Product.objects.filter(category__slug=slug,
                                          available=True).select_related(
            'brand').only('image', 'slug', 'brand', 'name', 'price', 'id')
    if obj == 'brand':
        products = Product.objects.filter(brand__slug=slug, available=True)

    if obj == 'subcategory':
        products = Product.objects.filter(
            subcategory__slug=slug,
            available=True).only('image', 'slug', 'brand', 'name', 'price', 'id')

    if obj == 'subcategorytype':
        products = Product.objects.filter(subcategory_type__slug=slug,
                                          available=True).only('image', 'slug', 'brand', 'name', 'price', 'id')
    category, subcategory, subcategory_type, sizes, brand = get_left_filter_submenu(products)
    return products, brand, category, subcategory, subcategory_type, sizes


def get_left_filter_submenu(product):
    """Получаем submenu для набора товаров"""
    category = Category.objects.filter(products__in=product).distinct('name').only('id', 'slug', 'name')
    subcategory = Subcategory.objects.filter(subcategory_products__in=product).distinct().only('id', 'slug', 'name')
    subcategory_type = SubcategoryType.objects.filter(subcategory_type_products__in=product). \
        distinct('name').only('id', 'slug', 'name')
    sizes = ProductSize.objects.filter(product__in=product).distinct('name').only('id', 'name')
    brands = Brand.objects.filter(product__in=product).distinct('name')
    return category, subcategory, subcategory_type, sizes, brands


def get_banners_for_index_page():
    """Получаем баннеры для главной страницы"""
    banners = Banner.objects.filter(is_actual=True)[:5]
    small_banners = SmallBanner.objects.filter(is_actual=True)[:5]
    return banners, small_banners


def get_new_items():
    """Получаем новые товары"""
    product = Product.objects.all()
    new_items = product.filter(created__gt=datetime.date.today() - datetime.timedelta(31)).values('image', 'slug')
    sales_items = product.filter(sale=True)[:5].values('image', 'slug')
    return new_items, sales_items


def get_sales_items():
    """Получаем товары со скидкой"""
    products = Product.objects.filter(available=True, sale=True).select_related(
        'brand').only('image', 'slug', 'brand', 'name', 'price', 'id')
    category, subcategory, subcategory_type, sizes, brands = get_left_filter_submenu(products)
    return subcategory, products, category, subcategory_type, brands, sizes


def get_new_articles():
    """Получаем новые статьи"""
    articles = Article.objects.all().order_by('created')[:3]
    return articles
