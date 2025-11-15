from apps.models.base import CreatedBaseModel, SlugBaseModel
from django.db import models
from django.db.models import (
    CASCADE,
    SET_NULL,
    BigIntegerField,
    ForeignKey,
    ImageField,
    JSONField,
    Model,
)
from django.db.models.fields import DateField, IntegerField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from drf_spectacular.utils import extend_schema_field
from mptt.models import MPTTModel, TreeForeignKey
from rest_framework import serializers


class Category(MPTTModel, SlugBaseModel):
    name = models.CharField(_('Name'), max_length=255)
    icon = ImageField(_('Icon'), upload_to='categories/icon/', blank=True, null=True)
    parent = TreeForeignKey('self', SET_NULL, null=True, blank=True, related_name='sub_categories',
                            verbose_name=_('Parent Category'))

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Product(SlugBaseModel, CreatedBaseModel):
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    description = CKEditor5Field(_('Description'))
    deliver_date = DateField(_('Delivery date'), null=True, blank=True)
    shop = ForeignKey(
        'apps.Shop',
        on_delete=CASCADE,
        related_name='products'
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']

    @property
    @extend_schema_field(serializers.FloatField())
    def price(self):
        versions = self.product_versions.all()
        if versions.exists():
            return min(v.final_price for v in versions)
        return None


class ProductVersion(SlugBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='product_versions')
    price = BigIntegerField(_('Price'))
    discount = IntegerField(_('Discount'), default=0)
    attributes = JSONField(_('Attributes'), null=True, blank=True)

    class Meta:
        verbose_name = _('product version')
        verbose_name_plural = _('product versions')

    @property
    def final_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price


class ProductImage(Model):
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
    image = ImageField(_('Image'), upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')


class Comment(CreatedBaseModel):
    product = ForeignKey('apps.Product', CASCADE)
    rate = IntegerField(_('Rate'), default=0)
    image = ImageField(_('Image'), upload_to='media/products/', null=True, blank=True)
    user = ForeignKey('apps.User', CASCADE)

    def __str__(self):
        return f"{self.rate}/5 | {self.product.name} uchun sharh"


class Like(Model):
    product = ForeignKey('apps.Product', CASCADE)
    user = ForeignKey('apps.User', CASCADE)

    class Meta:
        unique_together = ('product', 'user')
        default_related_name = 'likes'

    def __str__(self):
        return f"{self.user.phone} ❤️ {self.product.name}"
