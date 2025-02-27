from django.urls import path
from .views import geocode_view

urlpatterns = [
    path('geocode/', geocode_view, name='geocode'),
]
