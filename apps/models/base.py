import uuid

from django.db.models import Model, SlugField, UUIDField
from django.db.models.fields import DateTimeField


class UUIDBaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class CreatedBaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class SlugBaseModel(Model):
    slug = SlugField(max_length=255, editable=False, auto_created=True)


    class Meta:
        abstract = True