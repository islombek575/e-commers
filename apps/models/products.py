
from django.db.models import Model, ForeignKey, CASCADE, ImageField, BigIntegerField
from django.db.models.fields import CharField, DecimalField, IntegerField

from apps.models.base import UUIDBaseModel


class Category(Model):
    icon = ImageField(upload_to='categories/icon/')
    name = CharField(unique=True, max_length=255)



class Product(UUIDBaseModel):
    category = ForeignKey('apps.Category', on_delete=CASCADE)
    name = CharField(max_length=255)
    price = BigIntegerField()
    discount = IntegerField(default=0, null=True, blank=True)
    quantity = IntegerField(default=0)
    description = CharField(null=True, blank=True)
    size = CharField(max_length=100)
    color = CharField(max_length=100, null=True, blank=True)





class ProductImage(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    image = ImageField(upload_to='media/products/', null=True, blank=True)


class Like(Model):
    product = ForeignKey('apps.Product', on_delete=CASCADE)
    user = ForeignKey('apps.User', on_delete=CASCADE)

