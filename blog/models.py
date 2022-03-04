from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Содержимое')
    views_counter = models.PositiveIntegerField(verbose_name='Счетчик просмотров статьи', default=0)
    img = models.ImageField(upload_to='blogs', blank=True, null=True, verbose_name='Превью статьи')
    slug = models.SlugField(null=True, blank=True, max_length=50, verbose_name='Ссылка на статью')
    created = models.DateField(auto_now_add=True, verbose_name='Дата создания статьи')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})
