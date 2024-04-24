import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmorpg_fansite.settings')

app = Celery('mmorpg_fansite')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'fan_board.tasks.week_email_sending',
        'schedule': crontab(hour='8', minute='0', day_of_week='mon'),  # crontab(hour=0, minute=10, day_of_week=5),
    },
}
