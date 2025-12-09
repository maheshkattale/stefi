from product.models import *
from rest_framework import serializers
from datetime import datetime
from helpers.validations import hosturl
class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
class CustomProductSerializers(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()
    def get_brand_name(self, obj):
        obj_id = obj.brand_id
        
        if obj_id is not None and obj_id !='' and obj_id !='None':
            try:
                obj = ProductBrand.objects.filter(id=obj_id).first()
                if obj is not None:
                   return obj.name
                else:
                    return None
            except ProductBrand.DoesNotExist:
                return None
        return None
    color_name = serializers.SerializerMethodField()
    def get_color_name(self, obj):
        obj_id = obj.color_id
        
        if obj_id is not None and obj_id !='' and obj_id !='None':
            try:
                obj = ProductColor.objects.filter(id=obj_id).first()
                if obj is not None:
                   return obj.name
                else:
                    return None
            except ProductColor.DoesNotExist:
                return None
        return None
    size_unit_name = serializers.SerializerMethodField()
    def get_size_unit_name(self, obj):
        obj_id = obj.size_unit_id
        
        if obj_id is not None and obj_id !='' and obj_id !='None':
            try:
                obj = ProductSizeUnit.objects.filter(id=obj_id).first()
                if obj is not None:
                   return obj.name
                else:
                    return None
            except ProductSizeUnit.DoesNotExist:
                return None
        return None
    category_name = serializers.SerializerMethodField()
    def get_category_name(self, obj):
        obj_id = obj.category_id
        
        if obj_id is not None and obj_id !='' and obj_id !='None':
            try:
                obj = ProductCategory.objects.filter(id=obj_id).first()
                if obj is not None:
                   return obj.name
                else:
                    return None
            except ProductCategory.DoesNotExist:
                return None
        return None
    subcategory_name = serializers.SerializerMethodField()
    def get_subcategory_name(self, obj):
        obj_id = obj.subcategory_id
        
        if obj_id is not None and obj_id !='' and obj_id !='None':
            try:
                obj = ProductSubCategory.objects.filter(id=obj_id).first()
                if obj is not None:
                   return obj.name
                else:
                    return None
            except ProductSubCategory.DoesNotExist:
                return None
        return None
    vendor_name = serializers.SerializerMethodField()
    def get_vendor_name(self, obj):
        obj_id = obj.vendor_id
        
        if obj_id is not None and obj_id !='' and obj_id !='None':
            try:
                obj = Vendor.objects.filter(id=obj_id).first()
                if obj is not None:
                   return obj.name
                else:
                    return None
            except Vendor.DoesNotExist:
                return None
        return None
    product_image_url = serializers.SerializerMethodField()
    def get_product_image_url(self, obj):
        obj_id = obj.product_image
        
        if obj_id is not None and obj_id !='' and obj_id !='None':
            obj = hosturl+'/media/'+str(obj_id)
           
        else:
            obj=hosturl+'/static/assets/img/backgrounds/dummy.jpg'

        print("obj",obj)
        return obj
        
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


class CustomProductSubCategorySerializers(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductSubCategory
        fields = '__all__'

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

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

