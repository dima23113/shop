import os
from celery import Celery

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
}


#  celery -A projectshop flower worker -l info -P gevent
