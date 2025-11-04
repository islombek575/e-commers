from django.db.models import Model, ForeignKey, CASCADE, ImageField, BigIntegerField, JSONField
from django.db.models.fields import CharField, IntegerField, DateField, DateTimeField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.models.base import SlugBaseModel, CreatedBaseModel


class Category(SlugBaseModel):
    icon = ImageField(verbose_name=_('Icon'), upload_to='categories/icon/')
    name = CharField(verbose_name=_("Name"), unique=True, max_length=255)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class SubCategory(SlugBaseModel):
    icon = ImageField(verbose_name=_('Icon'), upload_to='subcategories/icon/')
    name = CharField(verbose_name=_("Name"), unique=True, max_length=255)
    category = ForeignKey('apps.Category', CASCADE, related_name='sub_categories')

    class Meta:
        verbose_name = _('sub category')
        verbose_name_plural = _('sub categories')


def __str__(self):
    return self.name


class Product(SlugBaseModel, CreatedBaseModel):
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    name = CharField(verbose_name=_('Name'), max_length=255)
    description = CKEditor5Field(verbose_name=_('Description'))
    deliver_date = DateField(verbose_name=_('Delivery date'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class ProductVersion(SlugBaseModel):
    product = ForeignKey('apps.Product', CASCADE)
    price = BigIntegerField(verbose_name=_('Price'))
    discount = IntegerField(verbose_name=_('Discount'), default=0)
    attributes = JSONField(verbose_name=_('Attributes'), null=True, blank=True)

    class Meta:
        verbose_name = _('product version')
        verbose_name_plural = _('product versions')

    @property
    @extend_schema_field(serializers.FloatField())
    def final_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price


class ProductImage(Model):
    product = ForeignKey('apps.Product', CASCADE)
    image = ImageField(verbose_name=_('Image'), upload_to='media/products/', null=True, blank=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')


class Comment(Model):
    product = ForeignKey('apps.Product', CASCADE)
    rate = IntegerField(verbose_name=_('Rate'), default=0)
    image = ImageField(verbose_name=_('Image'), upload_to='media/products/', null=True, blank=True)
    user = ForeignKey('apps.User', CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rate


class Like(Model):
    product = ForeignKey(Product, CASCADE, related_name='likes')
    user = ForeignKey('apps.User', CASCADE, related_name='likes')

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.phone} ❤️ {self.product.name}"
