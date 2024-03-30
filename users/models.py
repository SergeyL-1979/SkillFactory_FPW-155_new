from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models

from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"), max_length=150, unique=True, help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), db_index=True, max_length=150, blank=True)
    last_name = models.CharField(_("last name"), db_index=True, max_length=150, blank=True)
    email = models.EmailField(_("email"), db_index=True, max_length=60, unique=True)
    activation_code = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("Код подтверждения"))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        unique_together = ('email',)

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return "{}, ({})".format(self.email, self.get_full_name())

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip() if full_name.strip() else self.email

    def get_short_name(self):
        return self.first_name if self.first_name else self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

