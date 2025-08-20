from django.urls import path
from .views import *
# app_name = 'home_api'

urlpatterns = [
    path('search/', api_search_destinations, name='search_destinations'),
    path('states/', api_get_states, name='get_states'),
    path('popular-destinations/', api_get_popular_destinations, name='get_popular_destinations'),
    path('destination-types/', api_get_destination_types, name='get_destination_types'),
]