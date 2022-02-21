from django.db import models
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey
from sorl.thumbnail import ImageField
from account.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=256, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=256, unique=True, verbose_name='Слаг категории')
    line_num = models.IntegerField(blank=True, null=True, verbose_name='Порядок категорий в меню сайта')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', kwargs={'slug': self.slug})


class Subcategory(models.Model):
    name = models.CharField(max_length=256, verbose_name='Подкатегория')
    slug = models.SlugField(max_length=256, verbose_name='Слаг подкатегории')
    category = models.ForeignKey(Category, related_name='subcategories',
                                 on_delete=models.CASCADE, verbose_name='Категория')
    line_num = models.IntegerField(blank=True, null=True, verbose_name='Порядок подкатегорий в меню сайта')

    class Meta:
        ordering = ('line_num',)
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f'{self.category.name} - {self.name}'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_subcategory', args=[self.slug])


class SubcategoryType(models.Model):
    name = models.CharField(max_length=256, verbose_name='Тип подкатегории')
    slug = models.SlugField(max_length=256, verbose_name='Слаг типа подкатегории')
    subcategory = GroupedForeignKey(Subcategory, 'category', related_name='subcategory_type', on_delete=models.CASCADE,
                                    verbose_name='Подкатегория')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип подкатегории'
        verbose_name_plural = 'Тип подкатегории'

    def __str__(self):
        return f'{self.subcategory.name} - {self.name}'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_subcategory_type', args=[self.slug])


class Brand(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название бренда')
    slug = models.SlugField(max_length=256, verbose_name='Слаг бренда')
    image = models.ImageField(blank=True, upload_to='brand/', verbose_name='Лого бренда')
    description = models.TextField(verbose_name='Описание бренда')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand', kwargs={'slug': self.slug})


class Banner(models.Model):
    image = ImageField(upload_to='banners', verbose_name='Изображение баненра')
    is_actual = models.BooleanField(default=True, verbose_name='Актуальность баннера')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания баннера')
    banners = models.ForeignKey(Brand, related_name='big_brand_banner', on_delete=models.CASCADE,
                                verbose_name='Бренд для главной страницы', null=True, blank=True)
    is_sale_banner = models.BooleanField(default=False, verbose_name='Флаг распродажи без привязки к бренду')

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


class SmallBanner(models.Model):
    image = ImageField(upload_to='small_banner', verbose_name='Изображение маленького баннера')
    is_actual = models.BooleanField(default=True, verbose_name='Актуальность баннера')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания баннера')
    banners = models.ForeignKey(Brand, related_name='small_brand_banner', on_delete=models.CASCADE,
                                verbose_name='Бренд для главной страницы', null=True, blank=True)
    is_sale_banner = models.BooleanField(default=False, verbose_name='Флаг распродажи без привязки к бренду')

    class Meta:
        verbose_name = 'Маленький баннер'
        verbose_name_plural = 'Маленькие баннеры'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = GroupedForeignKey(Subcategory, 'category', on_delete=models.CASCADE, verbose_name='Подкатегория',
                                    related_name='subcategory_products')
    subcategory_type = GroupedForeignKey(SubcategoryType, 'subcategory', on_delete=models.CASCADE,
                                         verbose_name='Тип подкатегории',
                                         blank=True, null=True, related_name='subcategory_type_products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Название бренда')
    name = models.CharField(max_length=256, verbose_name='Название товара')
    slug = models.SlugField(max_length=256, verbose_name='Слаг товара')
    image_sizes = models.ImageField(upload_to='product_sizes_info/', blank=True, verbose_name='Размерная сетка товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    specifications = models.TextField(blank=True, null=True, verbose_name='Характеристики товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    available = models.BooleanField(default=True, verbose_name='Доступность товара')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    article = models.CharField(max_length=256, verbose_name='Артикул')
    type_of = models.CharField(max_length=256, verbose_name='Тип', blank=True)
    mark = models.CharField(max_length=256, verbose_name='Марка', blank=True)
    gender = models.CharField(max_length=256, verbose_name='Пол', null=True, blank=True)
    compound = models.CharField(max_length=256, verbose_name='Состав', blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='main_image', verbose_name='Главное изображение')
    favorite = models.ManyToManyField(CustomUser, through='Favorites', related_name='favorite')
    price_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                         verbose_name='Цена товара со скидкой')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.category.name} - {self.name}'

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})


class ImgProduct(models.Model):
    img = models.ImageField(verbose_name='Изображения товара', upload_to='product/')
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='product_img', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'

    def __str__(self):
        return f'Изображение для товара {self.product.name}'


class ProductSize(models.Model):
    name = models.CharField(max_length=256, verbose_name='Размер товара')
    qty = models.IntegerField(verbose_name='Количество')
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='product_sizer', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Размер товара'
        verbose_name_plural = 'Размеры товара'


class Favorites(models.Model):
    users = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    favorites = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Избранный товар')
    create = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.users.id}-{self.favorites.name}'
