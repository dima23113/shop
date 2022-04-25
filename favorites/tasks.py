from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task


@shared_task
def send_notification_for_favorites(user, products):
    """Метод отправляет информационное письмо по товару из избранного"""
    pass