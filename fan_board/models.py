from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.urls import reverse

from django.conf import settings
from django.utils.text import slugify

from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    """ Model for ad categories. """
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        """
        Сохраните объект, создав ярлык для имени, если оно еще не установлено.

        Параметры:
            *args: список аргументов переменной длины.
            **kwargs: произвольные аргументы ключевых слов.
        """
        if not self.name:
            self.name = slugify(str(self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """ Получить ссылку на объект """
        return reverse('category', kwargs={'pk': self.pk})


# ===== СИГНАЛ ДЛЯ СОЗДАНИЯ КАТЕГОРИЙ ПОСЛЕ МИГРАЦИИ =========
@receiver(post_migrate)
def create_initial_categories(sender, **kwargs):
    """
    Создайте начальные категории после применения миграции.

    Эта функция представляет собой приемник сигнала, который срабатывает после применения миграции.
    Он проверяет, является ли имя отправителя «fan_board», и если да, то создает начальные категории.
    путем перебора списка названий категорий. Для каждого имени категории он вызывает
    Метод get_or_create модели Category для создания или получения категории.

    Parameters:
        sender (Any): The sender of the signal.
        **kwargs (Any): Additional keyword arguments.

    Returns:
        None
    """
    if sender.name == "fan_board":
        categories = ['Tanks', 'Healers', 'Damage Dealers', 'Merchants',
                      'Guild masters', 'Quest givers', 'Blacksmiths', 'Tanners',
                      'Potions Masters', 'Spell Masters']
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
# =============================================================


class Advertisement(models.Model):
    """ MODEL FOR ADS """
    ad_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    ad_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    headline = models.CharField(max_length=100, verbose_name='Заголовок')
    content = CKEditor5Field(verbose_name='Полное описание', config_name='extends')
    image = models.ImageField(upload_to='img/', null=True, blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        """
        Returns a string representation of the object.

        :return: A string representing the headline of the object.
        :rtype: str
        """
        return f'{self.headline}'

    def get_absolute_url(self):
        """ Get a reference to an object. """
        return reverse('fan_board:ads_detail', kwargs={'headline': self.headline})


class Response(models.Model):
    """ MODEL FOR RESPONSES TO ADVERTISEMENTS """
    ad = models.ForeignKey(Advertisement, related_name='responses', on_delete=models.CASCADE)
    text = models.TextField()
    user_answer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='answer', verbose_name='Автор отклика')
    accepted_answer = models.BooleanField(default=False, verbose_name='Принять отклик')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the object.

        :return: A string representation of the object.
        :rtype: str
        """
        return f'{self.text}'

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.subscribed}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
