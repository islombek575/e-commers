import re

from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from jsonschema.exceptions import ValidationError

from apps.models.base import CreatedBaseModel
from apps.models.managers import UserManager


class User(AbstractUser):
    address = CharField(_('Location'), max_length=100, null=True, blank=True)
    phone = CharField(_('Phone Number'), max_length=15, unique=True)
    username = None
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def normalize_phone(self):
        if not self.phone:
            return None
        cleaned_phone = re.sub(r'[^0-9]', '', str(self.phone))
        if cleaned_phone.startswith('998') and len(cleaned_phone) == 12:
            return cleaned_phone[3:]
        if len(cleaned_phone) == 9:
            return cleaned_phone
        return cleaned_phone

    def clean(self):
        super().clean()
        normalized_phone = self.normalize_phone()
        if not normalized_phone:
            pass
        if normalized_phone and len(normalized_phone) != 9:
            raise ValidationError('Telefon raqami 9 ta raqamdan iborat bo\'lishi kerak')

        self.phone = normalized_phone

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.phone = self.normalize_phone()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.phone


class Market(CreatedBaseModel):
    name = CharField(_('Name'), max_length=100)
    banner = ImageField(_('Banner'), upload_to='market/banner/')
    logo = ImageField(_('Logo'), upload_to='market/logo/')
    description = CKEditor5Field(_('Description'))
