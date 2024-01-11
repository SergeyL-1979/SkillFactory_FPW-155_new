import random
import string

from allauth.account.adapter import get_adapter
from allauth.account.forms import LoginForm, SignupForm, BaseSignupForm
from allauth.core.internal.http import redirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.forms import (
    ModelForm, CharField, TextInput, EmailInput, PasswordInput, EmailField)
from django.core.exceptions import ValidationError
from django.urls import reverse

from users.models import CustomUser


class UserForm(ModelForm):
    """Модельная форма редактировать профиль"""

    class Meta:
        model = CustomUser

        fields = ['username', 'first_name', 'last_name', 'email', ]

        labels = {'username': 'Логин', 'first_name': 'Имя',
                  'last_name': 'Фамилия', 'email': 'email', }

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'width:40ch ',
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...',
                'style': 'width:40ch',
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...',
                'style': 'width:40ch',
            }),
            'email': EmailInput(attrs={
                'multiple class': 'form-control',
                'style': 'width:40ch',
            }),
        }

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        # Достать всех пользователей с таким email, кроме себя
        if CustomUser.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован')
        return email


class UserLoginForm(LoginForm):
    # условие для применения ACCOUNT_FORMS в settings
    """Переопределить форму вхожа allauth"""

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['login'] = CharField(
            label="E-MAIL", widget=TextInput(attrs={'class': 'form-control', }))
        self.fields['password'].widget = PasswordInput(
            attrs={'class': 'form-control', })


class UserRegistrationForm(SignupForm):
    # можно по разному переопределять форму. Так:
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           "type": "email",
                                                           "placeholder": "E-mail address",
                                                           "autocomplete": "email",
                                                           }))
    # Добавьте свои поля, если необходимо
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               "placeholder": "First",
                                                               "autocomplete": "first_name",
                                                               "type": "first_name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              "placeholder": "Last",
                                                              "type": "last_name",
                                                              "autocomplete": "last_name"}))

    def save(self, request):
        user = super(UserRegistrationForm, self).save(request)
        # Генерация временного пароля и сохранение в поле activation_code
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        user.activation_code = temp_password
        # Отправка временного пароля на почту пользователя
        subject = 'Активация аккаунта'
        message = f'Для активации вашего аккаунта используйте временный пароль: {temp_password}'
        user.email_user(subject, message)
        user.save()
        return user

    # @login_required
    # def send_activation_email(self, request):
    #     user = request.user
    #     subject = 'Активация учетной записи MMORPG'
    #     message = f'''
    #         Здравствуйте!
    #
    #         Вы зарегистрированы в сервисе MMORPG.
    #         Реквизиты для доступа в личный кабинет: https://example.com/
    #
    #         login: {user.email}
    #         password: {user.password}
    #     '''
    #     from_email = 'your-email@example.com'
    #     send_mail(subject, message, from_email, [user.email])
    #     return redirect('profile')
