
from django.urls import path
from . import views
app_name = 'masters_ui'



urlpatterns = [

    path('vendor_list', views.vendor_list, name='vendor_list'),
    path('vendor-list', views.vendor_list, name='vendor_list'),
    path('add-vendor',views.add_vendor, name='add_vendor'),



]