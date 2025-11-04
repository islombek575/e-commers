# orders.py
from django.db.models import CharField, ForeignKey, CASCADE, BigIntegerField, DateTimeField, IntegerField
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _

from apps.models.base import UUIDBaseModel, CreatedBaseModel


class Order(UUIDBaseModel, CreatedBaseModel):
    class OrderStatus(TextChoices):
        PENDING = 'PENDING', _('Pending Confirmation')
        PROCESSING = 'PROCESSING', _('Processing')
        DELIVERING = 'DELIVERING', _('On the way')
        DELIVERED = 'DELIVERED', _('Delivered')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELED = 'CANCELED', _('Canceled')
        RETURNED = 'RETURNED', _('Returned')

    class PaymentMethod(TextChoices):
        CARD = 'CARD', _('Card Online')
        CASH = 'CASH', _('Cash on Delivery')
        INSTALLMENT = 'INSTALLMENT', _('Installment Plan')

    customer = ForeignKey('apps.User', CASCADE, related_name='orders')
    status = CharField(default=OrderStatus.PENDING, max_length=20, choices=OrderStatus.choices,verbose_name=_('Order Status'))
    total_price = BigIntegerField(default=0, verbose_name=_('Total Price'))
    payment_method = CharField(max_length=20, choices=PaymentMethod.choices, verbose_name=_('Payment Method'))
    delivery_address = CharField(max_length=255, verbose_name=_('Delivery Address'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return f"Order {self.id} for {self.customer.phone}"


class OrderItem(UUIDBaseModel):
    order = ForeignKey('apps.Order', CASCADE, related_name='items')
    product_version = ForeignKey('apps.ProductVersion', CASCADE)
    quantity = IntegerField(default=1, verbose_name=_('Quantity'))
    price_at_purchase = BigIntegerField(verbose_name=_('Price at Purchase'))

    @property
    def total(self):
        return self.quantity * self.price_at_purchase

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return f"{self.product_version.product.name} ({self.quantity}x)"
