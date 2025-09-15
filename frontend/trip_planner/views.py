from django.shortcuts import render, redirect, HttpResponse
import requests
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from helpers.validations import hosturl

# API URLs
login_url = hosturl + "/api/User/login"
logout_url = hosturl + "/api/User/logout"
from rest_framework.response import Response

# Create your views here.
def plan_trip(request):
    """Admin panel login page"""
    print("holo")
    return render(request, 'customer/trips/plan-trip-form.html')
