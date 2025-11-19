"""
URL configuration for stefi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),

    # backend
    path('api/User/', include('User.urls')),
    path('api/Masters/', include('Masters.urls')),
    path('api/trips/', include('trips.urls')),
    path('api/home_api/', include('home_api.urls')),
    path('api/vendor/', include('vendor.urls')),
    path('api/product/', include('product.urls')),



    # frontend
    path('',include(('home.urls', 'home'),namespace='home')),
    path('trip_planner/', include(('trip_planner.urls', 'trip_planner'),namespace='trip_planner')),
    path('stefi-admin-pannel/', include(('admin_ui.urls', 'admin_ui'),namespace='admin_ui')),
    path('stefi-admin-dashboard/', include(('dashboard_ui.urls', 'dashboard_ui'),namespace='dashboard_ui')),
    path('stefi-admin-masters/', include(('masters_ui.urls', 'masters_ui'),namespace='masters_ui')),
    path('stefi-admin-product/', include(('product_ui.urls', 'product_ui'),namespace='product_ui')),
    path('stefi-admin-vendor/', include(('vendor_ui.urls', 'vendor_ui'),namespace='vendor_ui')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
