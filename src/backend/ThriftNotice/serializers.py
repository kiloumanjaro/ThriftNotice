# ThriftNotice/serializers.py
from rest_framework import serializers
from .models import ThriftStores, Users, FavoriteShop, UsersReview


class ThriftStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThriftStores
        fields = '__all__' # Or specify fields you want to expose in the API, e.g., ['id', 'title', 'content', 'created_at']

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__' # Or specify fields you want to expose in the API, e.g., ['id', 'title', 'content', 'created_at']

class FavoriteShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteShop
        fields = '__all__' # Or specify fields you want to expose in the API, e.g., ['id', 'title', 'content', 'created_at']

class UsersReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersReview
        fields = '__all__' # Or specify fields you want to expose in the API, e.g., ['id', 'title', 'content', 'created_at']