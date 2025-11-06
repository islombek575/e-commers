from apps.models.base import UUIDBaseModel
from django.db.models import CASCADE, BigIntegerField, ForeignKey, IntegerField
from django.utils.translation import gettext_lazy as _


class Cart(UUIDBaseModel):
    customer = ForeignKey('apps.User', CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of {self.customer.phone}"


class CartItem(UUIDBaseModel):
    cart = ForeignKey('apps.Cart', CASCADE, related_name='items')
    product_version = ForeignKey('apps.ProductVersion', CASCADE)
    quantity = IntegerField(_('Quantity'), default=1)
    price = BigIntegerField(_('Price at Addition'), default=0)

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product_version.product.name} ({self.quantity}x)"
