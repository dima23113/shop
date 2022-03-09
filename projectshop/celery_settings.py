import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectshop.settings')

app = Celery('projectshop')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Europe/London'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    pass
