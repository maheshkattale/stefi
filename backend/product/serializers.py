from product.models import *
from rest_framework import serializers
from datetime import datetime

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class ProductCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=ProductCategory
        fields='__all__'
class ProductSubCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=ProductSubCategory
        fields='__all__'
class ProductBrandSerializers(serializers.ModelSerializer):

    class Meta:
        model=ProductBrand
        fields='__all__'

class ProductSizeUnitSerializers(serializers.ModelSerializer):
    class Meta:
        model=ProductSizeUnit
        fields='__all__'
class ProductColorSerializers(serializers.ModelSerializer):
    class Meta:
        model=ProductColor
        fields='__all__'
class ProductMediaSerializers(serializers.ModelSerializer):
    class Meta:
        model=ProductMedia
        fields='__all__'
class ProductDetailSerializers(serializers.ModelSerializer):
    media = ProductMediaSerializers(many=True, read_only=True)
    class Meta:
        model=Product
        fields='__all__'

