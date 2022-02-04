from django.db import models


class TextEditor(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Содержимое')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return str(self.title)
