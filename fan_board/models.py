from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify

from django_ckeditor_5.fields import CKEditor5Field

from users.models import CustomUser


class Category(models.Model):
    """ Модель Category """
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = slugify(str(self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Получить ссылку на объект"""
        return reverse('category', kwargs={'pk': self.pk})


# ===== СИГНАЛ ДЛЯ СОЗДАНИЯ КАТЕГОРИЙ ПОСЛЕ МИГРАЦИИ =========
@receiver(post_migrate)
def create_initial_categories(sender, **kwargs):
    if sender.name == "fan_board":
        categories = ['Tanks', 'Healers', 'Damage Dealers', 'Merchants',
                      'Guild masters', 'Quest givers', 'Blacksmiths', 'Tanners',
                      'Potions Masters', 'Spell Masters']
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
# =============================================================


class Advertisement(models.Model):
    ad_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    ad_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    headline = models.CharField(max_length=100, verbose_name='Заголовок')
    content = CKEditor5Field(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        """ Строковое отображение объекта """
        return f'{self.headline}'

    def get_absolute_url(self):
        """ Получить ссылку на объект """
        return reverse('ad_detail', kwargs={'pk': self.pk})


class Response(models.Model):
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    text = models.TextField()
    user_answer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='answer', verbose_name='Автор отклика')
    accepted_answer = models.BooleanField(default=False, verbose_name='Принять отклик')
    notified = models.BooleanField(default=False, verbose_name='Уведомлен')
    created_at = models.DateTimeField(auto_now_add=True)
    # answer = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='answer',
    # verbose_name='Опубликовать ответ')
    # accepted_answer = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='accepted_answer',
    #                                          verbose_name='Принятый ответ')

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


# class PrivatePage(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
#     response = models.ForeignKey(Response, models.CASCADE, verbose_name='Отклик')
#
#     # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
#     # user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Приват'
#         verbose_name_plural = 'Приват'


