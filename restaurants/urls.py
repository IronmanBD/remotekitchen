from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantAPI, MenuAPI, MenuManageAPI, ItemAPI, ItemManageAPI

router = DefaultRouter()
router.register(r'restaurants', RestaurantAPI, basename='restaurant')

urlpatterns = [
    path('', include(router.urls)),
    path('restaurants/<int:pk>/menus/', MenuAPI.as_view(), name='menus'),
    path('restaurants/<int:pk>/menus/<int:menu_id>/', MenuManageAPI.as_view(), name='menu-manage'),
    path('restaurants/<int:pk>/menus/<int:menu_id>/items/', ItemAPI.as_view(), name='items'),
    path('restaurants/<int:pk>/menus/<int:menu_id>/items/<int:item_id>/', ItemManageAPI.as_view(), name='item-manege'),
]