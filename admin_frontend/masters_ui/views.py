from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
import os
import json
from datetime import datetime,date,timedelta
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import date
from helpers.validations import hosturl

# Create your views here.
get_hotel_list_url=hosturl+"/api/Masters/get-hotels-list"

# Create your views here.
def hotel_list(request):
    token = request.session.get('token',False)
    if token:
        data={}
        hotel_list_request = requests.post(get_hotel_list_url, data=data)
        hotel_list_response = hotel_list_request.json()

        return render(request, 'admin/hotels/hotel_list.html',{'hotels':hotel_list_response['data']})
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('admin_ui:login') # change this.
    
def hotel_add(request):
    token = request.session.get('token',False)
    if token:
        return render(request, 'admin/hotels/hotel_add.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('admin_ui:login') # change this.