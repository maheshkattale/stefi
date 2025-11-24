from django.urls import path
# from .api_views import trip_list, create_trip, trip_detail, add_itinerary_item, delete_itinerary_item, generate_invoice
from product.views import *
urlpatterns = [
    path('product_list', product_list, name='api_product_list'),
    path('product_list_pagination', product_list_pagination.as_view(), name='api_product_list_pagination'),
    

    # path('')
    path('add_product', add_product, name='api_add_product'),


    path('product_category_list', product_category_list, name='api_product_category_list'),
    path('product_category_list_pagination', product_category_list_pagination.as_view(), name='api_product_category_list_pagination'),
    path('add_product_category', add_product_category, name='api_add_product_category'),
    path('update_product_category', update_product_category, name='api_update_product_category'),
    path('delete_product_category', delete_product_category, name='api_delete_product_category'),
    path('product_category_by_id', product_category_by_id, name='api_product_category_by_id'),


    path('product_sub_category_list_pagination', product_sub_category_list_pagination.as_view(), name='api_product_sub_category_list_pagination'),
    path('product_subcategory_list', product_subcategory_list, name='api_product_subcategory_list'),
    path('add_product_subcategory', add_product_subcategory, name='api_add_product_subcategory'),
    path('update_product_subcategory', update_product_subcategory, name='api_update_product_subcategory'),
    path('delete_product_subcategory', delete_product_subcategory, name='api_delete_product_subcategory'),
    path('product_subcategory_by_id', product_subcategory_by_id, name='api_product_subcategory_by_id'), 



    path('product_brand_list', product_brand_list, name='api_product_brand_list'),
    path('add_product_brand', add_product_brand, name='api_add_product_brand'),
    path('update_product_brand', update_product_brand, name='api_update_product_brand'),
    path('delete_product_brand', delete_product_brand, name='api_delete_product_brand'),
    path('product_brand_by_id', product_brand_by_id, name='api_product_brand_by_id'),

    path('product_size_list_pagination', product_size_list_pagination.as_view(), name='api_product_size_list_pagination'),
    path('product_size_unit_list', product_size_unit_list, name='product_size_unit_list'),
    path('add_product_size_unit', add_product_size_unit, name='api_add_product_size_unit'),
    path('update_product_size_unit', update_product_size_unit, name='api_update_product_size_unit'),
    path('delete_product_size_unit', delete_product_size_unit, name='api_delete_product_size_unit'),
    path('product_size_unit_by_id', product_size_unit_by_id, name='api_product_size_unit_by_id'),


    path('product_color_list_pagination', product_color_list_pagination.as_view(), name='api_product_color_list_pagination'),

    path('product_color_list', product_color_list, name='api_product_color_list'),
    path('add_product_color', add_product_color, name='api_add_product_color'),
    path('update_product_color', update_product_color, name='api_update_product_color'),
    path('delete_product_color', delete_product_color, name='api_delete_product_color'),
    path('product_color_by_id', product_color_by_id, name='api_product_color_by_id'),


]