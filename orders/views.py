from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Orders, OrderItem
from orders.permissions import IsOwner, IsEmployee, IsCustomer
from orders.serializers import OrderSerializer
from restaurants.models import Restaurants, Items


# Create your views here.
class OrderAPI(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner|IsEmployee|IsCustomer]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        if self.request.user.role == 'owner':
            restaurants = Restaurants.objects.filter(owner=self.request.user)
            return Orders.objects.filter(restaurant__in=restaurants).prefetch_related('order_items__item')
        elif self.request.user.role == 'customer':
            return Orders.objects.filter(customer=self.request.user).prefetch_related('order_items__item')
        elif self.request.user.role == 'employee':
            restaurants = self.request.user.employee.all()
            return Orders.objects.filter(restaurant__in=restaurants).prefetch_related('order_items__item')

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = None
        if self.request.user.role == 'owner':
            restaurants = Restaurants.objects.filter(owner=self.request.user)
            order = Orders.objects.filter(restaurant__in=restaurants, id=order_id).prefetch_related('order_items__item').first()
        elif self.request.user.role == 'customer':
            order = Orders.objects.filter(customer=self.request.user, id=order_id).prefetch_related('order_items__item').first()
        elif self.request.user.role == 'employee':
            restaurants = self.request.user.employee.all()
            order = Orders.objects.filter(restaurant__in=restaurants, id = order_id).prefetch_related('order_items__item').first()

        if order is None:
            return Response({"MSG": "Order Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = get_object_or_404(Orders, id=order_id)

        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = get_object_or_404(Orders, id=order_id)

        item_id = request.query_params.get('item_id', None)
        print(item_id)
        if item_id:
            order_item = get_object_or_404(OrderItem, order=order, item=item_id)
            order_item.delete()
        else:
            order.delete()
        return Response({"MSG":"Content DELETED"},status=status.HTTP_204_NO_CONTENT)



