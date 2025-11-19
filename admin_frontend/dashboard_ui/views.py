from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
import requests
import os
import json
from datetime import datetime,date,timedelta
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import date
# from project.views import statuscheck
from rest_framework.response import Response
from helpers.validations import hosturl
from django.http import JsonResponse
# Create your views here.
# Create your views here.


forgot_password_url=hosturl+"/api/User/forgetpasswordmail"


def home(request):
    if request.method == 'POST':
        print("request.POST",request.POST)
        # email = request.POST['email']
        # password = request.POST['password']
        # data = {}
        # data['email'] = email
        # data['password'] = password
        # data['source'] = 'Mobile'

        # home_request = requests.post(home_url, data=data)
        # home_response = home_request.json()
        # print("home_response",home_response)
        # if home_response['response']['n'] == 1:
        #     token = home_response['data']['token']
        #     request.session['token'] = token 
        #     request.session['role_id'] = home_response['data']['role'] 
        #     request.session['role_name'] = home_response['data']['role_name']  
        #     request.session['user_name'] = home_response['data']['username']   
        #     return HttpResponse(json.dumps(home_response),content_type='application/json')
        # else:
        #     # messages.error(request, home_response['response']['msg'])
        #     return HttpResponse(json.dumps(home_response),content_type='application/json')
    else:
        return render(request, 'admin/dashboard/admin_dashboard.html')