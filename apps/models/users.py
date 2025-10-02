from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.db.models.fields import CharField


class UserProfile(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100, null=True, blank=True)
    address = CharField(max_length=100, null=True, blank=True)
    email = CharField(max_length=100, unique=True)
    phone = CharField(max_length=100, unique=True)
    password = CharField(max_length=100)
