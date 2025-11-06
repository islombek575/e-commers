import uuid

from django.db.models import (CharField, DateTimeField, Model, SlugField,
                              UUIDField)
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class UUIDBaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class CreatedBaseModel(Model):
    created_at = DateTimeField(_('Created_at'), auto_now_add=True)

    class Meta:
        abstract = True
        ordering = '-created_at',


class SlugBaseModel(Model):
    slug = SlugField(max_length=255, unique=True, editable=False)
    name = CharField(_("Name"), unique=True, max_length=255)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug and hasattr(self, "name"):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
