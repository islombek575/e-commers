from django.db.models import CASCADE, ForeignKey, IntegerField, BigIntegerField
from django.utils.translation import gettext_lazy as _

from apps.models.base import UUIDBaseModel


class Cart(UUIDBaseModel):
    customer = ForeignKey('apps.User', CASCADE, related_name='cart')
    total = BigIntegerField(default=0, verbose_name=_('Total Price'))

    def __str__(self):
        return f"Cart of {self.customer.phone}"


class CartItem(UUIDBaseModel):
    cart = ForeignKey('apps.Cart', CASCADE, related_name='items')
    product_version = ForeignKey('apps.ProductVersion', CASCADE)
    quantity = IntegerField(default=1, verbose_name=_('Quantity'))
    price = BigIntegerField(default=0, verbose_name=_('Price at Addition'))

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product_version.product.name} ({self.quantity}x)"
