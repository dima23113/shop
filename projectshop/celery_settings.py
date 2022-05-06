import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectshop.settings')

app = Celery('projectshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Europe/London'
app.conf.beat_schedule = {
    'every-30-seconds': {
        'task': 'orders.tasks.confirm_payment',
        'schedule': 30.0,
    },
    'every_first_and_third_weeks_of_the_month': {
        'task': 'loyalty_program.tasks.remove_user_bonuses',
        'schedule': crontab(),
    },
    'every_day_order_statistics': {
        'task': 'orders.tasks.get_order_statistics',
        'schedule': crontab(),
    },
    'ever_day_discount_check': {
        'task': 'discount_system.tasks.discount_check',
        'schedule': crontab(),
    },
    'ever_week_notification_for_favorites': {
        'task': 'favorites.tasks.send_notification_for_favorites',
        'schedule': crontab(),
    }

}
#  loyalty_program.tasks.remove_user_bonuses

#  celery -A projectshop flower worker -l info -P gevent
