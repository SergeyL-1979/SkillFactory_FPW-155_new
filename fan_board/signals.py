from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags

from fan_board.models import Response, Advertisement
from mmorpg_fansite import settings


@receiver(post_save, sender=Response)
def response_created(instance, **kwargs):
    print('Объявление', instance.ad.headline, 'создано')

    send_mail(
        subject='Написан отклик на объявление',
        message=f'На ваше объявление {instance.ad.headline} '
                f'был откликнувшийся {instance.user_answer.first_name}. '
                f'Ваш отклик: {instance.text}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.ad.ad_author.email],
    )


# ================================================================================
# # Отправляем уведомление на почту
# send_mail(
#     'Ваш отклик принят',
#     render_to_string('notification_email.txt', {'response': instance}),
#     settings.DEFAULT_FROM_EMAIL,
#     [instance.user_answer.email],
#     fail_silently=False,
# )

# Отправляем уведомление в телеграм
# send_mail(
#     'Ваш отклик принят',
#     render_to_string('notification_telegram.txt', {'response': instance}),
#     settings.DEFAULT_FROM_EMAIL,
#     [instance.user_answer.email],
#     fail_silently=False,
# )
