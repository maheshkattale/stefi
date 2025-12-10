from django.db import models
from helpers.models import TrackingModel
from django.db.models.deletion import CASCADE
from vendor.models import Vendor
class ProductCategory(TrackingModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProductSubCategory(TrackingModel):
    category = models.ForeignKey(ProductCategory, on_delete=CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProductBrand(TrackingModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class ProductSizeUnit(TrackingModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class ProductColor(TrackingModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(TrackingModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=CASCADE, related_name='products', blank=True, null=True)
    subcategory = models.ForeignKey(ProductSubCategory, on_delete=CASCADE, related_name='products', blank=True, null=True)
    brand = models.ForeignKey(ProductBrand, on_delete=CASCADE, related_name='products', blank=True, null=True)
    size_unit = models.ForeignKey(ProductSizeUnit, on_delete=CASCADE, related_name='products', blank=True, null=True)
    color = models.ForeignKey(ProductColor, on_delete=CASCADE, related_name='products', blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=CASCADE, related_name='products', blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    redirect_url = models.TextField(blank=True, null=True)
    product_image = models.FileField(upload_to='products/product_images/', blank=True, null=True)


    
    def __str__(self):
        return self.name
    
class ProductMedia(TrackingModel):  
    product = models.ForeignKey(Product, on_delete=CASCADE, related_name='media')
    media_file = models.FileField(upload_to='products/media_files/')
