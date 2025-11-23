
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

]