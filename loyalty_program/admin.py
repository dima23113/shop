from django.contrib import admin
from .models import *


@admin.register(BonusesProgram)
class BonusesProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'bonus_percentage', 'required_amount', 'validity_period']
    list_editable = ['bonus_percentage', 'required_amount', 'validity_period']


@admin.register(UserBonuses)
class UserBonusesAdmin(admin.ModelAdmin):
    list_display = ['user', 'bonuses', 'bonuses_program']
    list_filter = ['user', 'bonuses_program']
    list_editable = ['bonuses_program', 'bonuses']
