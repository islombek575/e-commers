from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.db.models.fields import CharField


class User(Model):
    name = CharField(max_length=100, null=True, blank=True)
    email = CharField(max_length=100, null=True, blank=True)
    phone = CharField(max_length=100, null=True, blank=True)




class AdminUser(AbstractUser):
    pass