
from django.db.models import Model, ForeignKey, CASCADE, ImageField
from django.db.models.fields import CharField, DecimalField, BooleanField


class Category(Model):
    name = CharField(unique=True)


class Product(Model):
    name = CharField(max_length=100)
    price = DecimalField(decimal_places=2, max_digits=10)
    discount_price = DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    color = CharField(max_length=100, null=True, blank=True)
    in_stock = BooleanField(default=True)
    description = CharField(null=True, blank=True)


class ProductImage(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    image = ImageField(upload_to='media/products/', null=True, blank=True)
