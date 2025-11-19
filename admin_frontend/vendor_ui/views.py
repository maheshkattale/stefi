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