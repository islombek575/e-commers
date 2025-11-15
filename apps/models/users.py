import re

from apps.models.base import CreatedBaseModel
from apps.models.managers import UserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    BooleanField,
    ForeignKey,
    ImageField,
    OneToOneField,
    TextChoices,
)
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from jsonschema.exceptions import ValidationError


class User(AbstractUser):
    class Role(TextChoices):
        admin = 'admin'
        moderator = 'moderator'
        merchant = 'merchant.json'
        client = 'client'

    address = CharField(_('Location'), max_length=100, null=True, blank=True)
    role = CharField(_('Role'), max_length=100, choices=Role.choices, default=Role.client)
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


class Merchant(CreatedBaseModel):
    user = OneToOneField('apps.User', CASCADE, limit_choices_to={'role': 'merchant.json'},
                         related_name='merchant_profile',
                         verbose_name=_('User'))
    company_name = CharField(_('Company Name'), max_length=150)
    tin = CharField(_('STIR / INN'), max_length=15, unique=True)
    logo = ImageField(_('Logo'), upload_to='merchant.json/logos/', null=True, blank=True)
    description = CKEditor5Field(_('Description'), null=True, blank=True)
    is_verified = BooleanField(_('Is Verified ?'), default=False)

    def __str__(self):
        return self.company_name


class Shop(CreatedBaseModel):
    merchant = ForeignKey('apps.Merchant', CASCADE, related_name='markets', verbose_name=_('Merchant'))
    name = CharField(_('Name'), max_length=100)
    banner = ImageField(_('Banner'), upload_to='market/banner/')
    logo = ImageField(_('Logo'), upload_to='market/logo/')
    description = CKEditor5Field(_('Description'))

    def __str__(self):
        return self.name
