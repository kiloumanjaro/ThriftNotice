from django.shortcuts import render

# Create your views here.
# ThriftNotice/views.py
from rest_framework import viewsets
from .models import ThriftStores
from .serializers import ThriftStoreSerializer

class ThriftStoreViewSet(viewsets.ModelViewSet):
    queryset = ThriftStores.objects.all() #  Get all Notice objects
    serializer_class = ThriftStoreSerializer # Use the NoticeSerializer
