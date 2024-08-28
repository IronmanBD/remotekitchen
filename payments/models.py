from django.db import models

from orders.models import Orders


# Create your models here.
class Payment(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    checkout_session_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=20)
    amount = models.FloatField()


    def __str__(self):
        return f"{self.order}-{self.amount}--{self.payment_status}"

    class Meta:
        db_table = 'payments'
