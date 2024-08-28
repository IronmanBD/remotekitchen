from django.conf import settings
from django.db import models

from restaurants.models import Restaurants, Items


# Create your models here.
class Orders(models.Model):
    ORDER_STATUS = (
        ('open', 'Open'),
        ('processing', 'Processing'),
        ('complete', 'Complete')
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, related_name='restaurant')
    date = models.DateField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='open')

    @property
    def calculate_total(self, ):
        return sum(item.item.price*item.quantity for item in self.order_items.all())

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='item')
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.order}-{self.item}-{self.quantity}"

    class Meta:
        db_table = 'orderitems'




