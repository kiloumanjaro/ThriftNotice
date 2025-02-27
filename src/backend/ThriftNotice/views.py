from django.shortcuts import render

# Create your views here.
# ThriftNotice/views.py
from rest_framework import viewsets
from .models import ThriftStores, Users
from .serializers import ThriftStoreSerializer, UsersSerializer

class ThriftStoreViewSet(viewsets.ModelViewSet):
    queryset = ThriftStores.objects.all() #  Get all Notice objects
    serializer_class = ThriftStoreSerializer # Use the NoticeSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all() #  Get all Notice objects
    serializer_class = UsersSerializer # Use the NoticeSerializer
