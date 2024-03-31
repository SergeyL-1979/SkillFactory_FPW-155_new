import random
import string
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        # Генерация временного пароля
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            activation_code=temp_password,  # Сохранение временного пароля в поле activation_code
            **extra_fields
        )
        user.is_active = False  # для активации пользователя по ссылке надо установить False по умолчанию
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user
