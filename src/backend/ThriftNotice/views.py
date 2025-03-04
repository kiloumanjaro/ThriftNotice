from django.shortcuts import render

# Create your views here.
# ThriftNotice/views.py
from rest_framework import viewsets
from .models import ThriftStores, Users, FavoriteShop, UsersReview
from .serializers import ThriftStoreSerializer, UsersSerializer, FavoriteShopSerializer, UsersReviewSerializer
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
        queryset = self.queryset.values('latitude', 'longitude', 'shopid', 'shopname', 'formattedaddress', 'shortdescription') # Efficiently select lat/long, andshopid, and Shopname
        return Response(list(queryset), status=status.HTTP_200_OK)
    
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all() #  Get all Notice objects
    serializer_class = UsersSerializer # Use the NoticeSerializer

    @action(detail=False, methods=['get'], url_path='get_user')
    def get_user(self, request):
        username = request.GET.get("username")
        user = Users.objects.filter(username=username).first()

        if user is None:
            return Response({"error": "User not found"}, status=404)

        return Response(UsersSerializer(user).data)
    
    @action(detail=False, methods=['get'], url_path='get_userid')
    def get_userid(self, request):
        userid = request.GET.get("userid")
        user = Users.objects.filter(userid=userid).first()

        if user is None:
            return Response({"error": "User not found"}, status=404)

        return Response(UsersSerializer(user).data)
    

class FavoriteShopViewSet(viewsets.ModelViewSet):
    queryset = FavoriteShop.objects.all() #  Get all Notice objects
    serializer_class = FavoriteShopSerializer # Use the NoticeSerializer

    @action(detail=False, methods=['get'], url_path='get_favorite_shops')
    def get_favorite_shops(self, request):
        userid = request.GET.get("userid")

        # Find all favorite shops for the given userid
        favorite_shops = FavoriteShop.objects.filter(userid=userid)

        if not favorite_shops.exists():
            return Response({"error": "No favorite shops found for this user"}, status=404)

        # Extract all shop IDs from the favorites
        shopid = favorite_shops.values_list('shopid', flat=True)

        # Query the Shop table to get addresses
        shops = ThriftStores.objects.filter(shopid__in=shopid).values('shopname', 'formattedaddress')

        return Response(list(shops))
    
    @action(detail=False, methods=['delete'], url_path='delete_favorite_shop')
    def delete_favorite_shop(self, request):
        userid = request.GET.get("userid")
        shopid = request.GET.get("shopid")

        # Try to find and delete the favorite shop entry
        deleted_count, _ = FavoriteShop.objects.filter(userid=userid, shopid=shopid).delete()

        if deleted_count == 0:
            return Response({"error": "No matching favorite shop found"}, status=404)

        return Response({"message": "Favorite shop deleted successfully"}, status=200)

class UsersReviewViewSet(viewsets.ModelViewSet):
    queryset = UsersReview.objects.all() #  Get all Notice objects
    serializer_class = UsersReviewSerializer # Use the NoticeSerializer

    @action(detail=False, methods=['get'], url_path='get_reviews')
    def get_reviews(self, request):
        shopid = request.GET.get("shopid")
        reviews = UsersReview.objects.filter(shopid=shopid)

        if not reviews.exists():
            return Response({"error": "no reviews found"}, status=404)

        return Response(UsersReviewSerializer(reviews, many = True).data)
        