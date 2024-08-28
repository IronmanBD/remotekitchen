from rest_framework import serializers

from orders.models import OrderItem, Orders


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'item', 'quantity']
        read_only_fields = ['order']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Orders
        fields = ['id', 'customer', 'restaurant', 'order_status', 'order_items']
        read_only_fields = ['id']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Orders.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', None)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.restaurant = validated_data.get('restaurant', instance.restaurant)
        instance.order_status = validated_data.get('order_status', instance.order_status)
        instance.save()

        if order_items_data:
            OrderItem.objects.filter(order=instance).delete()
            for item_data in order_items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance

