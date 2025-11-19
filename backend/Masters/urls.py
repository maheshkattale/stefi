from django.urls import path
from .views import *
# app_name = 'home_api'

urlpatterns = [

    path('addstate', addstate.as_view(), name = 'addstate'),
    path('adddestination', adddestination.as_view(), name = 'adddestination'),
    path('updatedestination', updatedestination.as_view(), name = 'updatedestination'),

    path('get-hotels-list', gethotelslist.as_view(), name = 'gethotelslist'),
    path('hotel_list_pagination_api', hotel_list_pagination_api.as_view(), name = 'hotel_list_pagination_api'),
    path('add-hotel', addhotel.as_view(), name='add-hotel'),
    path('get-hotel-types', get_hotel_types.as_view(), name='get-hotel-types'),
    path('get-destinations', get_destinations.as_view(), name='get-destinations'),


]