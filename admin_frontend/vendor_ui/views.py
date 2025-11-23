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
def vendor_list(request):
    token = request.session.get('token',False)
    if token:

        return render(request, 'admin/vendor/vendor-list.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def add_vendor(request):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            print("jii")
            data=request.POST.copy()
            add_vendor_url=hosturl+"/api/vendor/add_vendor"

            add_vendor_request = requests.post(add_vendor_url, data=data,headers=headers,files=request.FILES)
            add_vendor_response = add_vendor_request.json()
            return HttpResponse(json.dumps(add_vendor_response),content_type='application/json')
        else:
            return render(request, 'admin/vendor/add-vendor.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def edit_vendor(request,id):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':

            data=request.POST.copy()

            edit_vendor_url=hosturl+"/api/vendor/update_vendor"
            edit_vendor_request = requests.post(edit_vendor_url, data=data,headers=headers,files=request.FILES)
            edit_vendor_response = edit_vendor_request.json()
            return HttpResponse(json.dumps(edit_vendor_response),content_type='application/json')
        else:
            data={'id':id}
            get_vendor_details_url=hosturl+"/api/vendor/vendor_by_id"
            get_vendor_details_request = requests.post(get_vendor_details_url, data=data,headers=headers)
            get_vendor_details_response = get_vendor_details_request.json()
            print("get_vendor_details_response",get_vendor_details_response)
            return render(request, 'admin/vendor/edit-vendor.html',{'vendor':get_vendor_details_response['data']})
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    