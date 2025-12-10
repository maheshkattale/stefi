
from django.urls import path
from . import views
app_name = 'masters_ui'



urlpatterns = [
    path('product-category-list', views.product_category_list, name='product-category_list'),
    path('add-product-category',views.add_product_category, name='add_product-category'),
    path('edit-product-category/<str:id>',views.edit_product_category, name='edit_product-category'),


    path('product-sub-category-list', views.product_sub_category_list, name='product-sub-category_list'),
    path('add-product-sub-category',views.add_product_sub_category, name='add_product-sub-category'),
    path('edit-product-sub-category/<str:id>',views.edit_product_sub_category, name='edit_product-sub-category'),

    path('product-brand-list', views.product_brand_list, name='product-brand_list'),
    path('add-product-brand',views.add_product_brand, name='add_product-brand'),
    path('edit-product-brand/<str:id>',views.edit_product_brand, name='edit_product-brand'),


    path('product-size-list', views.product_size_list, name='product-size_list'),
    path('add-product-size',views.add_product_size, name='add_product-size'),
    path('edit-product-size/<str:id>',views.edit_product_size, name='edit_product-size'),


    path('product-color-list', views.product_color_list, name='product-color_list'),
    path('add-product-color',views.add_product_color, name='add_product-color'),
    path('edit-product-color/<str:id>',views.edit_product_color, name='edit_product-color'),



    path('product-list', views.product_list, name='product_list'),
    path('add-product',views.add_product, name='add_product'),
    path('edit-product/<str:id>',views.edit_product, name='edit_product'),

]