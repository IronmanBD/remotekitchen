from django.conf import settings
from django.db import models

# Create your models here.
class Restaurants(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    employee = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='employee')

    class Meta:
        db_table = 'restaurants'

    def __str__(self):
        return f"{self.owner}-{self.name}"


class Menus(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'menus'

    def __str__(self):
        return f"{self.restaurant}-{self.name}"


class Items(models.Model):
    menu = models.ForeignKey(Menus, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=20)
    price = models.FloatField()
    is_available = models.BooleanField()


    class Meta:
        db_table = 'items'

    def __str__(self):
        return f"{self.menu}-{self.name}-{self.is_available}"
