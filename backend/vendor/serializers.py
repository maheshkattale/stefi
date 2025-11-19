
from rest_framework import serializers
from vendor.models import *
from datetime import datetime

class VendorSerializers(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields='__all__'