from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from .models import Advertisement
from users.models import CustomUser


@shared_task
def send_weekly_newsletter():
    # Определите категории объявлений, которые вы хотите включить в рассылку
    categories = ['Недвижимость', 'Транспорт', 'Работа']  # Пример категорий

    # Определите дату начала недели
    start_date = timezone.now() - timezone.timedelta(days=7)

    # Получите все объявления за последнюю неделю в указанных категориях
    new_ads = Advertisement.objects.filter(category__in=categories, created_at__gte=start_date)

    # Получите список зарегистрированных пользователей
    users = CustomUser.objects.all()

    for user in users:
        # Формируем контент для письма
        context = {
            'user': user,
            'new_ads': new_ads,
        }

        # Отправляем письмо
        subject = 'Еженедельная рассылка новостей'
        message = render_to_string('notification_email.html', context)
        user_email = user.email
        send_mail(subject, message, 'noreply@example.com', [user_email])

    print("Weekly newsletter sent successfully!")