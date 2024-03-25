from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.forms import (
    ModelForm, CharField, TextInput, EmailInput, PasswordInput, EmailField)
from django.core.exceptions import ValidationError

from users.models import CustomUser


class UserForm(ModelForm):
    """ Модельная форма редактировать профиль """

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', ]
        labels = {'username': 'Логин', 'first_name': 'Имя',
                  'last_name': 'Фамилия', 'email': 'email', }
        widgets = {'username': TextInput(attrs={
            'class': 'form-control', 'readonly': 'readonly',
            'style': 'width:40ch ',
        }),
            'first_name': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите текст...',
                'style': 'width:40ch',
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Введите текст...',
                'style': 'width:40ch',
            }),
            'email': EmailInput(attrs={
                'multiple class': 'form-control', 'placeholder': 'Введите email...',
                'style': 'width:40ch',
            }),
        }

    def clean_email(self):
        """ Проверка уникальности email """
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
            label="E-mail", widget=TextInput(attrs={'class': 'form-control', }))
        self.fields['password'].widget = PasswordInput(
            attrs={'class': 'form-control', })


class UserRegistrationForm(SignupForm):
    # Можно по-разному переопределять форму. Так:
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      "type": "email",
                                      "placeholder": "E-mail address",
                                      "autocomplete": "email",
                                      }))
    # Добавьте свои поля, если необходимо
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      "placeholder": "First",
                                      "autocomplete": "first_name",
                                      "type": "first_name"}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      "placeholder": "Last",
                                      "type": "last_name",
                                      "autocomplete": "last_name"}))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(username=email.split('@')[0]).exists():
            raise ValidationError("This username is already taken.")
        return email

    def save(self, request, commit=True):
        # Сначала вызываем метод save родительского класса
        user = super(UserRegistrationForm, self).save(request)
        # Затем сохраняем дополнительные данные
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['email'].split('@')[0]
        if commit:
            user.save()
        return user

    # TODO - реализовать активацию по коду при регистрации или в ТелеграмБот
    # # Генерация временного пароля и сохранение в поле activation_code
    # temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    # user.activation_code = temp_password
    # # Отправка временного пароля на почту пользователя
    # subject = 'Активация аккаунта'
    # message = f'Для активации вашего аккаунта используйте временный пароль: {temp_password}'
    # user.email_user(subject, message)

    # def verify_code(self, request):
    #     if self.request.method == 'POST':
    #         email = request.POST.get('email')
    #         code = request.GET.get('code')
    #         try:
    #             user = CustomUser.objects.get(email=email)
    #             if user.activation_code == code:
    #                 return render(
    #                     request, 'users/profile.html', {'user': user})
    #             else:
    #                 return render(request, 'invalid.html')
    #         except CustomUser.DoesNotExist:
    #             return render(request, 'user_not_found.html')
    #
    #     return render(request, 'verification_form.html')
