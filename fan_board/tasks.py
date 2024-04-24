from datetime import timedelta, date

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from fan_board.models import Advertisement
from mmorpg_fansite import settings
from users.models import CustomUser


@shared_task
def send_weekly_newsletter():
    week = timedelta(days=7)
    ads = Advertisement.objects.all()
    advertisement_week_ads = []
    template = 'weekly_digest.html'
    email_subject = 'Your News Portal Weekly Digest'

    for ad in ads:
        if ad.created_at >= date.today() - week:
            advertisement_week_ads.append(ad)

    for user in CustomUser.objects.all():
        if user.email:
            html_message = render_to_string(template, {'advertisement_week_ads': advertisement_week_ads})
            send_mail(email_subject, 'Weekly digest', settings.EMAIL_HOST_USER, [user.email], html_message=html_message)

# =========
