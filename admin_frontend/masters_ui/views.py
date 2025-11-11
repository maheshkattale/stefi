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
    
def add_hotel(request):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            data=request.POST.copy()
            add_hotel_url=hosturl+"/api/Masters/add-hotel"

            add_hotel_request = requests.post(add_hotel_url, data=data,headers=headers,files=request.FILES)
            add_hotel_response = add_hotel_request.json()
            print("add_hotel_response",add_hotel_response)
            return HttpResponse(json.dumps(add_hotel_response),content_type='application/json')
        else:
            return HttpResponse({
            "data" : [],
            "response":{
                "n":0,
                "msg":"Method not  allowed",
                "status":"error"
                }
        })
    else:
        return HttpResponse({
            "data" : [],
            "response":{
                "n":0,
                "msg":"Token is invalid",
                "status":"error"
                }
        })
def hotel_add(request):
    token = request.session.get('token',False)
    if token:
        return render(request, 'admin/hotels/hotel_add.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('admin_ui:login') # change this.