
from django.db.models import Model, ForeignKey, CASCADE, ImageField
from django.db.models.fields import CharField, DecimalField, IntegerField


class Category(Model):
    icon = ImageField(upload_to='media/icon/') # TODO categories/icon/
    name = CharField(unique=True) # TODO max_length=255
    # TODO slug


class Product(Model):
    category = ForeignKey('apps.Category', on_delete=CASCADE)
    name = CharField(max_length=255)
    price = DecimalField(decimal_places=2, max_digits=10)
    discount_price = DecimalField(decimal_places=2, max_digits=10, null=True, blank=True) # TODO chegirma foizi bolishi kk
    stock = IntegerField()
    description = CharField(null=True, blank=True)
    size = CharField(max_length=100)
    color = CharField(max_length=100, null=True, blank=True)





class ProductImage(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    image = ImageField(upload_to='media/products/', null=True, blank=True) # TODO .webp otkazish

