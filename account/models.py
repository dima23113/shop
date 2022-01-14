from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    zip_code = models.CharField(max_length=6, verbose_name='Индекс', null=True, blank=True)
    address = models.CharField(max_length=256, verbose_name='Адрес', blank=True, null=True)
    city = models.CharField(max_length=256, verbose_name='Город', blank=True, null=True)
    country = models.CharField(max_length=256, verbose_name='Стана', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
