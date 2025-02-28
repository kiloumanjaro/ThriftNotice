# ThriftNotice/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import ThriftStoreViewSet, UsersViewSet, FavoriteShopViewSet

router = routers.DefaultRouter()
router.register(r'thriftstores', ThriftStoreViewSet, basename='thriftstores') # 'ThriftStores' will be the URL path segment
router.register(r'Users', UsersViewSet, basename='users') # 'Users' will be the URL path segment
router.register(r'favoriteshop', FavoriteShopViewSet, basename='favoriteshop') # 'favoriteshop' will be the URL path segment


urlpatterns = [
    path('', include(router.urls)),
]