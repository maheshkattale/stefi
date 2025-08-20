from django.urls import path
# from .api_views import trip_list, create_trip, trip_detail, add_itinerary_item, delete_itinerary_item, generate_invoice
from .views import *
urlpatterns = [
    path('list', trip_list, name='api_trip_list'),
    path('create', create_trip, name='api_create_trip'),
    path('detail/<int:trip_id>', trip_detail, name='api_trip_detail'),
    path('itinerary/add', add_itinerary_item, name='api_add_itinerary_item'),
    path('itinerary/delete/<int:item_id>', delete_itinerary_item, name='api_delete_itinerary_item'),
    path('invoice/generate/<int:trip_id>', generate_invoice, name='api_generate_invoice'),
]