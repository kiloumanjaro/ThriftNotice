# ThriftNotice/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import ThriftStoreViewSet

router = routers.DefaultRouter()
router.register(r'thriftstores', ThriftStoreViewSet, basename='thriftstores') # 'ThriftStores' will be the URL path segment

urlpatterns = [
    path('', include(router.urls)),
]