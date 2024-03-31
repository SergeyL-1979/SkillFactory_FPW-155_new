from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from fan_board.models import Response
from mmorpg_fansite import settings


@receiver(post_save, sender=Response)
def response_created(sender, created, instance, **kwargs):

    if created:
        print('Объявление', instance.ad.headline, 'создано')
        domain = settings.DOMAIN_NAME
        send_mail(
            subject='Новый отклик на ваше объявление',
            message=f'На ваше объявление {instance.ad.headline} '
                    f'был откликнувшийся {instance.user_answer.first_name}. '
                    f'Ваш отклик: {instance.text} '
                    f'Link to your response: <a href="{domain}{instance.ad.get_absolute_url()}>cancel</a>',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.ad.ad_author.email],
        )


@receiver(post_save, sender=Response)
def send_notification_email(sender, instance, created, **kwargs):
    if instance.accepted_answer:
        print('Отклик принят')
        subject = 'Отклик принят'
        message = f'Ваш отклик на объявление "{instance.ad.headline}" был принят.'
        from_email = settings.DEFAULT_FROM_EMAIL  # Замените на свой email
        to_email = instance.ad.ad_author.email
        send_mail(subject, message, from_email, [to_email])
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
