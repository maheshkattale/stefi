from django.urls import path
from . import views
from home_api.views import api_search_destinations, api_get_states, api_get_popular_destinations, api_get_destination_types
app_name = 'home'

urlpatterns = [
    # Template rendering URLs
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('customer-registration/', views.customer_registration, name='customer_registration'),


    # Admin routes
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/create/', views.create_trip, name='create_trip'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trips/<int:trip_id>/invoice/', views.generate_invoice, name='generate_invoice'),
    path('trips/<int:trip_id>/invoice/view/', views.view_invoice, name='view_invoice'),
    path('itinerary/<int:item_id>/delete/', views.delete_itinerary_item, name='delete_itinerary_item'),
    
    path('state/<str:state>', views.state_details, name='state_details'),

    path('indian-states', views.indian_states, name='indian_states'),

    path('api/search/', api_search_destinations, name='api_search'),
    path('api/states/', api_get_states, name='api_states'),
    path('api/popular-destinations/', api_get_popular_destinations, name='api_popular_destinations'),
    path('api/destination-types/', api_get_destination_types, name='api_destination_types'),



]