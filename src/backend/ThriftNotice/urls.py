# ThriftNotice/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import ThriftStoreViewSet, UsersViewSet, FavoriteShopViewSet, UsersReviewViewSet

router = routers.DefaultRouter()
router.register(r'thriftstores', ThriftStoreViewSet, basename='thrift_stores') # 'thriftStores' will be the URL path segment
router.register(r'users', UsersViewSet, basename='users') # 'users' will be the URL path segment
router.register(r'favoriteshop', FavoriteShopViewSet, basename='favorite_shop') # 'favoriteshop' will be the URL path segment
router.register(r'usersreview', UsersReviewViewSet, basename='users_review') # 'usersreview' will be the URL path segment

urlpatterns = [
    path('', include(router.urls)),
]