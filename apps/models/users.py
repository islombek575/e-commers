import re

from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from jsonschema.exceptions import ValidationError

from apps.managers import UserManager


class User(AbstractUser):
    address = CharField(verbose_name=_('Location'), max_length=100, null=True, blank=True)
    phone = CharField(verbose_name=_('Phone Number'), max_length=15, unique=True)
    username = None
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def check_phone(self):
        digits = re.findall(r'\d', self.phone)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')

        phone = ''.join(digits)
        self.phone = phone.removeprefix('998')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.check_phone()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


def __str__(self):
    return self.phone
