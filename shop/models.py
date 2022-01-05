from django.db import models
from django.urls import reverse


class Category(models.Model):

    name = models.CharField(max_length=256, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=256, unique=True, verbose_name='Слаг категории')

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
    slug = models.SlugField(max_length=256, verbose_name='Слог подкатегории')
    category = models.ForeignKey(Category, related_name='subcategories',
                                 on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:

        ordering = ('name',)
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f'{self.category.name} - {self.name}'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_subcategory', args=[self.slug])


class Brand(models.Model):

    name = models.CharField(max_length=256, verbose_name='Название бренда')
    slug = models.SlugField(max_length=256, verbose_name='Слаг бренда')
    image = models.ImageField(blank=True, upload_to='brand/', verbose_name='Лого бренда')
    description = models.CharField(max_length=256, verbose_name='Описание бренда')

    class Meta:

        ordering = ('name',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand', kwargs={'slug': self.slug})


class Product(models.Model):

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегория')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Название бренда')
    name = models.CharField(max_length=256, verbose_name='Название товара')
    slug = models.SlugField(max_length=256, verbose_name='Слаг товара')
    image_sizes = models.ImageField(upload_to='product_sizes_info/', blank=True, verbose_name='Изображения товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    available = models.BooleanField(default=True, verbose_name='Доступность товара')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    article = models.CharField(max_length=256, verbose_name='Артикул')
    type_of = models.CharField(max_length=256, verbose_name='Тип', blank=True)
    mark = models.CharField(max_length=256, verbose_name='Марка', blank=True)
    gender = models.CharField(max_length=256, verbose_name='Пол')
    compound = models.CharField(max_length=256, verbose_name='Состав', blank=True)

    class Meta:

        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.category.name} - {self.name}'

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


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
