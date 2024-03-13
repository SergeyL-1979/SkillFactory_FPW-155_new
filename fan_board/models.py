from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse

from django_ckeditor_5.fields import CKEditor5Field

from users.models import CustomUser


# User = get_user_model()
class Category(models.IntegerChoices):
    Tanks = 1, 'Tanks'
    Healers = 2, 'Healers'
    DD = 3, 'Damage Dealers'
    Merchants = 4, 'Merchants'
    GuildMasters = 5, 'Guild masters'
    QuestGivers = 6, 'Quest givers'
    Blacksmiths = 7, 'Blacksmiths'
    Tanners = 8, 'Tanners'
    Potions_Masters = 9, 'Potions Masters'
    Spell_Masters = 10, 'Spell Masters'


class Advertisement(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор', related_name='advertisements')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = CKEditor5Field(blank=True, verbose_name='Текст объявления')
    # category = models.PositiveSmallIntegerField(choices=Category.choices, verbose_name='Категория')
    category = models.SlugField(max_length=5, choices=Category.choices, verbose_name='Категория')

    # category = models.CharField(max_length=50, choices=[
    #     ('Tanks', 'Tanks'),
    #     ('Healers', 'Healers'),
    #     ('DD', 'Damage Dealers'),
    #     ('Merchants', 'Merchants'),
    #     ('Guild masters', 'Guild masters'),
    #     ('Quest givers', 'Quest givers'),
    #     ('Blacksmiths', 'Blacksmiths'),
    #     ('Tanners', 'Tanners'),
    #     ('Potions Masters', 'Potions Masters'),
    #     ('Spell Masters', 'Spell Masters'),
    # ])

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        """ Строковое отображение поста """
        return f'{self.title}'

    def get_absolute_url(self):
        """ Получить ссылку на объект """
        return reverse('ads_detail', kwargs={'pk': self.pk})


class Response(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    text = models.TextField()
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'{self.text}'
