from django.urls import path
from .views import *
# app_name = 'home_api'

urlpatterns = [

    path('addstate', addstate.as_view(), name = 'addstate'),
    path('adddestination', adddestination.as_view(), name = 'adddestination'),
    path('updatedestination', updatedestination.as_view(), name = 'updatedestination'),

    path('get-hotels-list', gethotelslist.as_view(), name = 'gethotelslist'),



]