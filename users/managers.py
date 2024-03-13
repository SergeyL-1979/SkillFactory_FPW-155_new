# from django.contrib.auth.models import BaseUserManager
#
#
# # Здесь должен быть менеджер для модели Юзера.
# # Поищите эту информацию в рекомендациях к проекту
# # Менеджер должен содержать как минимум две следующие функции
# class UserManager(BaseUserManager):
#     """
#     Функция создания пользователя — в нее мы передаем обязательные поля
#     """
#     def create_user(self, email, first_name, last_name, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             **extra_fields
#         )
#         user.is_active = False  # для активации пользователя по ссылке надо установить False по умолчанию
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_superuser', True)
#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             password=password,
#             **extra_fields,
#         )
#         user.is_active = True
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def activate_user(self, activation_code):
#         try:
#             user = self.get(activation_code=activation_code)
#             user.is_active = True
#             user.save()
#             return user
#         except self.model.DoesNotExist:
#             return None
