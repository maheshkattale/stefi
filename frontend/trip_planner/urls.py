# trip_planner/urls.py
from django.urls import path
from . import views

app_name = 'trip_planner'

urlpatterns = [
    path('plan_trip/', views.plan_trip, name='plan_trip'),
    # … other paths
]
