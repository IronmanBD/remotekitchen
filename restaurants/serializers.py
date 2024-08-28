from rest_framework import serializers
from .models import Restaurants, Menus, Items


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = ['id', 'name', 'owner', 'address']
        read_only_fields = ['id', 'owner']

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = ['id', 'restaurant', 'name']
        read_only_fields = ['id', 'restaurant']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'menu', 'name', 'price', 'is_available']
        read_only_fields = ['id', 'menu']

