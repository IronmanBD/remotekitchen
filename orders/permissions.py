from rest_framework import permissions
from rest_framework.permissions import BasePermission

from restaurants.models import Restaurants


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.role == 'owner':
            if request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']:
                return True
        return False



class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.role == 'employee':
            if request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']:
                return True
        return False



class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.role == 'customer':
                return True
        return False



