# ThriftNotice/serializers.py
from rest_framework import serializers
from .models import ThriftStores, Users


class ThriftStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThriftStores
        fields = '__all__' # Or specify fields you want to expose in the API, e.g., ['id', 'title', 'content', 'created_at']

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__' # Or specify fields you want to expose in the API, e.g., ['id', 'title', 'content', 'created_at']