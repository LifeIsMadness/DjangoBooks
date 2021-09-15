import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')

app = Celery('mywebsite')
app.config_from_object('django.conf:settings')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.broker_transport_options = {'visibility_timeout': 3600}
app.autodiscover_tasks(settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'products.tasks.send_verification_email',
        'schedule': crontab(),
    },

}

app.conf.timezone = 'UTC'
