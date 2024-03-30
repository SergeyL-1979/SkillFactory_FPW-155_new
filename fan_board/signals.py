from django.core.mail import send_mail
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags

from fan_board.models import Response, Advertisement
from mmorpg_fansite import settings


@receiver(post_save, sender=Advertisement)
def product_created(instance, **kwargs):
    print('Объявление', instance.headline, 'создано')

# @receiver(post_save, sender=Advertisement)
# def notify_new_response(sender, created, instance, **kwargs):
#     if created == "post_add":
#         for user in instance.accepted_answer.all():
#             msg = EmailMultiAlternatives(
#                 subject=instance.headline,
#                 body=instance.content,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to='mailto:{}'.format(user.email),
#             )
#             msg.attach_alternative(
#                 render_to_string(
#                     'fan_board/email_template.html',
#                     {
#                         'ad': instance,
#                         'user': user
#                     }
#                 ),
#                 'text/html'
#             )
#             msg.send()



# ================================================================================
# @receiver(post_save, sender=Response)
# def send_notification(sender, instance, created, **kwargs):
#     print(created, instance.ad.ad_author.email, instance.user_answer.email)
#     if not created and instance.notified:
#         ad = instance.ad
#         subject = 'Отклик на ваше объявление'
#         message = f'На ваше объявление "{ad}" поступил новый отклик от пользователя {instance.user_answer.username}.'
#         recipient_list = [ad.ad_author.email]  # Замените на ваш способ получения адреса электронной почты пользователя объявления
#         print(recipient_list)
#         send_mail(subject, message, None, recipient_list)

# @receiver(pre_save, sender=Response)
# def send_notification_email(sender, instance, action, **kwargs):
#     print(action, instance.user_answer.email)
    # if action == 'post_add':
    #     msg = EmailMultiAlternatives(
    #         subject=instance.headline,
    #         body=instance.post_text,
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         to='mailto:{}'.format(instance.user_answer.email),
    #     )
    #     msg.attach_alternative(
    #         render_to_string('notification_email.txt', {'response': instance}),
    #         'text/plain'
    #     )
    #     msg.send()
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

