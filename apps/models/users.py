from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.db.models.fields import CharField


class User(AbstractUser):
    address = CharField(max_length=100, null=True, blank=True)
    phone = CharField(max_length=100, unique=True)
