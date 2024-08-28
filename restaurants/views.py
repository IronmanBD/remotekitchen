from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.permissions import IsCustomer
from restaurants.models import Restaurants, Menus, Items
from restaurants.permissions import IsOwner, IsEmployee
from restaurants.serializers import RestaurantSerializer, MenuSerializer, ItemSerializer


# Create your views here.
class RestaurantAPI(ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsOwner|IsEmployee|IsCustomer]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'owner':
            return Restaurants.objects.filter(owner=user)
        if user.role == 'employee':
            return Restaurants.objects.filter(employee__in=[user])
        if user.role == 'customer':
            return Restaurants.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        restaurant = self.get_object()
        if self.request.user == restaurant.owner:
            serializer.save()
        return PermissionDenied("Only Owner Can Modify")

    def perform_delete(self, instance):
        restaurant = self.get_object()
        if self.request.user != restaurant.owner:
            return PermissionDenied("Only Owner Can Delete")
        instance.delete()
        return Response({"MSG":"DELETE SUCCESSFUL"}, status=status.HTTP_204_NO_CONTENT)


class MenuAPI(ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsOwner|IsEmployee|IsCustomer]

    def get_restaurant(self):
        restaurant_id = self.kwargs['pk']
        try:
            return Restaurants.objects.get(id=restaurant_id)
        except Restaurants.DoesNotExist:
            return Response({"MSG":"Restaurant Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        restaurant = self.get_restaurant()
        if restaurant:
            if self.request.user == restaurant.owner or restaurant.employee.filter(id=self.request.user.id).exists():
                return Menus.objects.filter(restaurant=restaurant)
            elif self.request.user.role=='customer':
                return Menus.objects.filter(restaurant=restaurant)


    def perform_create(self, serializer):
        restaurant = self.get_restaurant()
        if self.request.user == restaurant.owner:
            serializer.save(restaurant=restaurant)


class MenuManageAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsOwner|IsEmployee|IsCustomer]

    def get_restaurant(self):
        restaurant_id = self.kwargs['pk']
        try:
            return Restaurants.objects.get(id=restaurant_id)
        except Restaurants.DoesNotExist:
            return Response({"MSG":"Restaurant Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get_menu(self):
        restaurant = self.get_restaurant()
        menu_id = self.kwargs['menu_id']
        try:
            return Menus.objects.get(id=menu_id, restaurant=restaurant)
        except Menus.DoesNotExist:
            return Response({"MSG":"Menu Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        restaurant = self.get_restaurant()
        menu = self.get_menu()
        if restaurant:
            if self.request.user == restaurant.owner or restaurant.employee.filter(id=self.request.user.id).exists():
                return Menus.objects.filter(restaurant=restaurant, id=menu.id)
            elif self.request.user.role=='customer':
                return Menus.objects.filter(restaurant=restaurant, id=menu.id)

    def get(self, request, *args, **kwargs):
        menu = self.get_menu()
        if menu:
            serializer = self.get_serializer(menu)
            return Response(serializer.data)
        return Response({"MSG": "Menu Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        menu = self.get_menu()
        restaurant = self.get_restaurant()

        if self.request.user != restaurant.owner:
            raise PermissionDenied("Only the owner can update this menu.")

        serializer = self.get_serializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        menu = self.get_menu()
        restaurant = self.get_restaurant()

        if self.request.user != restaurant.owner:
            raise PermissionDenied("Only the owner can update this menu.")

        menu.delete()
        return Response({"MSG":"DELETE SUCCESSFUL"}, status=status.HTTP_204_NO_CONTENT)


class ItemAPI(ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsOwner|IsEmployee|IsCustomer]

    def get_restaurant(self):
        restaurant_id = self.kwargs['pk']
        try:
            return Restaurants.objects.get(id=restaurant_id)
        except Restaurants.DoesNotExist:
            return Response({"MSG":"Restaurant Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get_menu(self):
        menu_id = self.kwargs['menu_id']
        restaurant = self.get_restaurant()
        try:
            return Menus.objects.get(id=menu_id, restaurant=restaurant)
        except Menus.DoesNotExist:
            return Response({"MSG":"Menu Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        restaurant = self.get_restaurant()
        menu = self.get_menu()
        if restaurant and menu:
            if self.request.user == restaurant.owner or self.request.user in restaurant.employee.all():
                print("A")
                return Items.objects.filter(menu=menu)
            elif self.request.user.role == "customer":
                return Items.objects.filter(menu=menu)
            else:
                raise PermissionDenied("You do not have permission to view items in this menu.")

    def perform_create(self, serializer):
        menu = self.get_menu()
        restaurant = self.get_restaurant()

        if restaurant.owner == self.request.user or self.request.user in restaurant.employee.all():
            serializer.save(menu=menu)


class ItemManageAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsOwner|IsEmployee]

    def get_restaurant(self):
        restaurant_id = self.kwargs['pk']
        try:
            return Restaurants.objects.get(id=restaurant_id)
        except Restaurants.DoesNotExist:
            return Response({"MSG":"Restaurant Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get_menu(self):
        menu_id = self.kwargs['menu_id']
        restaurant = self.get_restaurant()
        try:
            return Menus.objects.get(id=menu_id, restaurant=restaurant)
        except Menus.DoesNotExist:
            return Response({"MSG":"Menu Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get_item(self):
        item_id = self.kwargs['item_id']
        menu = self.get_menu()
        try:
            return Items.objects.get(id=item_id, menu=menu)
        except Menus.DoesNotExist:
            return Response({"MSG":"Menu Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        item = self.get_item()
        if item:
            serializer = self.get_serializer(item)
            return Response(serializer.data)
        return Response({"MSG": "Item Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def perform_update(self, serializer):
         menu = self.get_menu()
         restaurant = self.get_restaurant()

         if self.request.user == restaurant.owner or self.request.user in restaurant.employee.all():
             serializer.save()

    def perform_destroy(self, instance):
         restaurant = self.get_restaurant()
         if self.request.user == restaurant.owner or self.request.user in restaurant.employee.all():
             instance.delete()
