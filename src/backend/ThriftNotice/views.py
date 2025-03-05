from django.shortcuts import render
from rest_framework import viewsets
from .models import ThriftStores, Users, FavoriteShop, UsersReview
from .serializers import ThriftStoreSerializer, UsersSerializer, FavoriteShopSerializer, UsersReviewSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class ThriftStoreViewSet(viewsets.ModelViewSet):
    queryset = ThriftStores.objects.all()
    serializer_class = ThriftStoreSerializer

    def _wrap_response(self, data, status_code=status.HTTP_200_OK, error=None):
        """Consistent response wrapper."""
        response_data = {"data": data} if data is not None else {"data": None}
        if error:
            response_data["error"] = error
        return Response(response_data, status=status_code)

    @action(detail=False, methods=['get'], url_path='map-locations')
    def map_locations(self, request):
        queryset = ThriftStores.objects.all()
        serializer = ThriftStoreSerializer(queryset, many=True) # Use serializer for list
        return self._wrap_response(serializer.data)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def _wrap_response(self, data, status_code=status.HTTP_200_OK, error=None):
        """Consistent response wrapper."""
        response_data = {"data": data} if data is not None else {"data": None}
        if error:
            response_data["error"] = error
        return Response(response_data, status=status_code)

    @action(detail=False, methods=['get'], url_path='user') # Consistent URL path
    def get_user_by_username(self, request): # More descriptive action name
        username = request.GET.get("username")
        user = Users.objects.filter(username=username).first()

        if user is None:
            return self._wrap_response(None, status_code=status.HTTP_404_NOT_FOUND, error="User not found")

        serializer = UsersSerializer(user)
        return self._wrap_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user-id') # Consistent URL path
    def get_user_by_id(self, request): # More descriptive action name
        userid = request.GET.get("userid")
        user = Users.objects.filter(userid=userid).first()

        if user is None:
            return self._wrap_response(None, status_code=status.HTTP_404_NOT_FOUND, error="User not found")

        serializer = UsersSerializer(user)
        return self._wrap_response(serializer.data)


class FavoriteShopViewSet(viewsets.ModelViewSet):
    queryset = FavoriteShop.objects.all()
    serializer_class = FavoriteShopSerializer

    def _wrap_response(self, data, status_code=status.HTTP_200_OK, error=None):
        """Consistent response wrapper."""
        response_data = {"data": data} if data is not None else {"data": None}
        if error:
            response_data["error"] = error
        return Response(response_data, status=status_code)


    @action(detail=False, methods=['get'], url_path='favorite-shops') # Consistent URL path
    def get_favorite_shops_by_user(self, request): # More descriptive action name
        userid = request.GET.get("userid")
        favorite_shops = FavoriteShop.objects.filter(userid=userid)

        if not favorite_shops.exists():
            return self._wrap_response(None, status_code=status.HTTP_404_NOT_FOUND, error="No favorite shops found for this user")

        shop_ids = favorite_shops.values_list('shopid', flat=True)
        shops = ThriftStores.objects.filter(shopid__in=shop_ids)
        serializer = ThriftStoreSerializer(shops, many=True) # Use serializer for list

        return self._wrap_response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='favorite-shop') # Consistent URL path
    def delete_favorite_shop(self, request):
        userid = request.GET.get("userid")
        shopid = request.GET.get("shopid")

        deleted_count, _ = FavoriteShop.objects.filter(userid=userid, shopid=shopid).delete()

        if deleted_count == 0:
            return self._wrap_response(None, status_code=status.HTTP_404_NOT_FOUND, error="No matching favorite shop found")

        return self._wrap_response({"message": "Favorite shop deleted successfully"}) # Data can be a dict or list

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
        