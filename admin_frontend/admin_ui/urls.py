
from django.urls import path
from . import views



urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('users_list', views.users_list, name='users_list'),

]