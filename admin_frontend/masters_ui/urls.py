
from django.urls import path
from . import views
app_name = 'masters_ui'



urlpatterns = [
    path('hotel_list', views.hotel_list, name='hotel_list'),
    path('hotels/add', views.hotel_add, name='hotel_add'),
    path('add_hotel', views.add_hotel, name='add_hotel'),

    # path('hotels/<int:pk>/edit', views.hotel_edit, name='hotel_edit'),
    # path('hotels/<int:pk>/delete', views.hotel_delete, name='hotel_delete'),


]