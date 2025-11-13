from django.db.models import ForeignKey, CASCADE, TextChoices, CharField
from django.db.models.fields import IntegerField

from apps.models.base import CreatedBaseModel


class Order(CreatedBaseModel):
    class Status(TextChoices):
        IN_PROGRESS = "in_progress", 'In Progress'
        CANCELLED = "cancelled", 'Cancelled'
        COMPLETED = "completed", 'Completed'

    status = CharField(max_length=15, choices=Status.choices, default=Status.IN_PROGRESS)
    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    total_amount = IntegerField()


class OrderItem(CreatedBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='order_items')
    order = ForeignKey('apps.Order', CASCADE, related_name='order_items')
    quantity = IntegerField(db_default=1)
    price = IntegerField()