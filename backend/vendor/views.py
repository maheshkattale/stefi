from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from django.utils import timezone
from product.serializers import *
from .serializers import *
from .models import *
import json
from django.db.models import Q
# from num2words import num2words
from django.db.models import Sum, IntegerField,FloatField
from django.db.models.functions import Cast
from decimal import Decimal, ROUND_DOWN
import math
from datetime import date, datetime
from time import strftime
from vendor.models import *
from vendor.serializers import *
from product.serializers import *
from helpers.validations import hosturl
from django.utils.timezone import now
import locale
from dateutil.relativedelta import relativedelta
import random
from rest_framework import pagination
from rest_framework.generics import GenericAPIView
from helpers.custom_functions import CustomPagination


# Create your views here.
class vendor_list_pagination(GenericAPIView):
    pagination_class = CustomPagination
    def post(self, request):
        vendors_obj = Vendor.objects.filter(isActive=True).order_by('name')
        if vendors_obj.exists():
            page4 = self.paginate_queryset(vendors_obj)
            serializer=VendorSerializers(page4,many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return self.get_paginated_response([])
        

@api_view(['GET'])
def vendor_list(request):
    vendors_obj = Vendor.objects.filter(isActive=True).order_by('name')
    if vendors_obj.exists():
        serializer=VendorSerializers(vendors_obj,many=True)
        return Response({"response":{"n":1,"msg":"Vendor list fetched successfully","status":"success"},"data":serializer.data})
    else:
        return Response({"response":{"n":1,"msg":"No vendors found","status":"success"},"data":[]})
        


@api_view(['POST'])
def add_vendor(request):
    data = request.data.copy()

    # Check duplicate name
    if Vendor.objects.filter(name__iexact=data.get('name'), isActive=True).exists():
        return Response({"response":{"n":0,"msg":"Vendor with this name already exists","status":"error"}})

    # Check duplicate email (since it's unique)
    if Vendor.objects.filter(email__iexact=data.get('email')).exists():
        return Response({"response":{"n":0,"msg":"Vendor with this email already exists","status":"error"}})

    # Check duplicate vendor_code only if provided
    if data.get("vendor_code"):
        if Vendor.objects.filter(vendor_code__iexact=data.get("vendor_code")).exists():
            return Response({"response":{"n":0,"msg":"Vendor code already exists","status":"error"}})

    data['isActive'] = True
    serializer = VendorSerializers(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({"response":{"n":1,"msg":"Vendor added successfully","status":"success"},"data":serializer.data})
    
    # error format
    first_key, first_value = next(iter(serializer.errors.items()))
    msg = first_key.upper() + ": " + str(first_value[0])
    return Response({"response":{"n":0,"msg":msg,"status":"error"},"errors":serializer.errors})



@api_view(['POST'])
def update_vendor(request):
    data = request.data.copy()
    vendor_id = data.get('id')

    try:
        vendor = Vendor.objects.get(id=vendor_id, isActive=True)
    except Vendor.DoesNotExist:
        return Response({"response":{"n":0,"msg":"Vendor not found","status":"error"}})

    # Name duplicate check
    if Vendor.objects.filter(name__iexact=data.get('name'), isActive=True).exclude(id=vendor_id).exists():
        return Response({"response":{"n":0,"msg":"Vendor with this name already exists","status":"error"}})

    # Email duplicate check
    if data.get("email"):
        if Vendor.objects.filter(email__iexact=data.get('email')).exclude(id=vendor_id).exists():
            return Response({"response":{"n":0,"msg":"Vendor with this email already exists","status":"error"}})

    # Vendor code duplicate check
    if data.get("vendor_code"):
        if Vendor.objects.filter(vendor_code__iexact=data.get("vendor_code")).exclude(id=vendor_id).exists():
            return Response({"response":{"n":0,"msg":"Vendor code already exists","status":"error"}})

    serializer = VendorSerializers(vendor, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"response":{"n":1,"msg":"Vendor updated successfully","status":"success"},"data":serializer.data})

    first_key, first_value = next(iter(serializer.errors.items()))
    msg = first_key.upper() + ": " + str(first_value[0])
    return Response({"response":{"n":0,"msg":msg,"status":"error"},"errors":serializer.errors})
   

@api_view(['POST'])
def delete_vendor(request):
    data = request.data.copy()
    vendor_id = data.get('id')
    try:
        vendor_obj = Vendor.objects.get(id=vendor_id, isActive=True)
    except Vendor.DoesNotExist:
        return Response({"response":{"n":0,"msg":"Vendor not found","status":"error"}})
    
    vendor_obj.isActive = False
    vendor_obj.save()
    return Response({"response":{"n":1,"msg":"Vendor deleted successfully","status":"success"}})


@api_view(['POST'])
def vendor_by_id(request):
    data = request.data.copy()
    print("data",data)
    vendor_id = data.get('id')
    try:
        vendor_obj = Vendor.objects.get(id=vendor_id, isActive=True)
    except Vendor.DoesNotExist:
        return Response({"response":{"n":0,"msg":"Vendor not found","status":"error"}})
    
    serializer = VendorSerializers(vendor_obj)
    return Response({"response":{"n":1,"msg":"Vendor fetched successfully","status":"success"},"data":serializer.data})




























