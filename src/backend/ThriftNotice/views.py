from django.shortcuts import render

# Create your views here.
# ThriftNotice/views.py
from rest_framework import viewsets
from .models import ThriftStores, Users
from .serializers import ThriftStoreSerializer, UsersSerializer
from rest_framework.decorators import action # Import the @action decorator
from rest_framework.response import Response
from rest_framework import status

class ThriftStoreViewSet(viewsets.ModelViewSet):
    queryset = ThriftStores.objects.all() #  Get all Notice objects
    serializer_class = ThriftStoreSerializer # Use the NoticeSerializer

    @action(detail=False, methods=['get'], url_path='map-locations') # Define a new action
    def map_locations(self, request):
        """
        Custom action to retrieve only latitude and longitude for map display.
        URL will be: /api/thriftstores/map-locations/ (because detail=False)
        """
        queryset = self.queryset.values('latitude', 'longitude', 'shopid') # Efficiently select lat/long
        return Response(list(queryset), status=status.HTTP_200_OK)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all() #  Get all Notice objects
    serializer_class = UsersSerializer # Use the NoticeSerializer
