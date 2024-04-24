from datetime import timedelta, datetime

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from fan_board.models import Advertisement
from mmorpg_fansite import settings
from users.models import CustomUser


@shared_task
def week_email_sending():
    start_date = timezone.now() - timedelta(days=7)
    ads = Advertisement.objects.filter(created_at__gte=start_date)
    advertisement_week_ads = list(ads)
    print(advertisement_week_ads, '[INFO] - ads list')
    template = 'weekly_digest.html'
    email_subject = 'Your News Portal Weekly Digest'

    for user in CustomUser.objects.all():
        if user.email:
            html_message = render_to_string(template, {'advertisement_week_ads': advertisement_week_ads})
            send_mail(email_subject, 'Weekly digest', settings.EMAIL_HOST_USER,
                      fail_silently=False, recipient_list=[user.email],
                      html_message=html_message)
