from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

from account.models import CustomUser

from celery import shared_task


@shared_task
def send_notification_for_favorites():
    """Метод отправляет информационное письмо по товару из избранного"""
    for user in CustomUser.objects.filter(favorites__isnull=False).distinct():
        fav = user.favorite.filter(sale=True)
        context = {
            'user': user,
            'favorites': fav
        }
        html_template = render_to_string(template_name='favorites/favorites_discount_alert.html', context=context)
        html_template = strip_tags(html_template)
        subject = 'Скидка на товар из изрбранного'
        send_mail(subject, html_template, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)
