from django.contrib import admin
from .models import Ticket, TicketMessage


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'status', 'indicator']
    list_filter = ['user', 'status', 'subject']


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'msg']
    list_filter = ['ticket']
