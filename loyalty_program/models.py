from django.db import models
from account.models import CustomUser


class BonusesProgram(models.Model):
    name = models.CharField(max_length=56, verbose_name='Название бонусной программы')
    bonus_percentage = models.PositiveIntegerField(verbose_name='% начисления бонусов с каждой покупки')
    required_amount = models.PositiveIntegerField(verbose_name='Требуемая сумма покупок')
    validity_period = models.PositiveIntegerField(verbose_name='Срок действия бонусов(дн)')

    class Meta:
        verbose_name = 'Бонусная программа'
        verbose_name_plural = 'Бонусные программы'

    def __str__(self):
        return self.name


class UserBonuses(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Бонусы пользователя',
                             related_name='user_bonuses')
    bonuses = models.PositiveIntegerField(verbose_name='Количество бонусов', default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата появления бонусов')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления ко-ва бонусов')
    bonuses_program = models.ForeignKey(BonusesProgram, on_delete=models.SET_NULL, verbose_name='Бонусная программа',
                                        null=True)

    class Meta:
        verbose_name = 'Бонусы пользователя'
        verbose_name_plural = 'Бонусы пользователей'

    def __str__(self):
        return f'{self.user.email} - {self.bonuses_program.name}'
