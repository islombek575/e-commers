from apps.models.base import CreatedBaseModel, SlugBaseModel
from django.db.models import CASCADE, BigIntegerField, ForeignKey, ImageField, JSONField, Model
from django.db.models.fields import DateField, DateTimeField, IntegerField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class Category(SlugBaseModel):
    icon = ImageField(_('Icon'), upload_to='categories/icon/')
    parent = ForeignKey('apps.Category', CASCADE, null=True, blank=True, related_name='sub_categories')

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Product(SlugBaseModel, CreatedBaseModel):
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    description = CKEditor5Field(_('Description'))
    deliver_date = DateField(_('Delivery date'), null=True, blank=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class ProductVersion(SlugBaseModel):
    product = ForeignKey('apps.Product', CASCADE)
    price = BigIntegerField(_('Price'))
    discount = IntegerField(_('Discount'), default=0)
    attributes = JSONField(_('Attributes'), null=True, blank=True)

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
        return f"{self.rate}/5 | {self.product.name} uchun sharh"


class Like(Model):
    product = ForeignKey(Product, CASCADE, related_name='likes')
    user = ForeignKey('apps.User', CASCADE, related_name='likes')

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.phone} ❤️ {self.product.name}"
