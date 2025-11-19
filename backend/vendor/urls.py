from django.urls import path
# from .api_views import trip_list, create_trip, trip_detail, add_itinerary_item, delete_itinerary_item, generate_invoice
from .views import *
urlpatterns = [
    path('vendor_list', vendor_list, name='api_vendor_list'),
    path('vendor_list_pagination', vendor_list_pagination.as_view(), name='api_vendor_list_pagination'),
    path('add_vendor', add_vendor, name='api_add_vendor'),
    path('update_vendor', update_vendor, name='api_update_vendor'),
    path('delete_vendor', delete_vendor, name='api_delete_vendor'),
    path('vendor_by_id', vendor_by_id, name='api_vendor_by_id'),

]