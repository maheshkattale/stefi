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
def product_category_list(request):
    token = request.session.get('token',False)
    if token:

        return render(request, 'admin/product_category/product-category-list.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def add_product_category(request):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            print("jii")
            data=request.POST.copy()
            add_product_category_url=hosturl+"/api/product/add_product_category"

            add_product_category_request = requests.post(add_product_category_url, data=data,headers=headers,files=request.FILES)
            add_product_category_response = add_product_category_request.json()
            return HttpResponse(json.dumps(add_product_category_response),content_type='application/json')
        else:
            return render(request, 'admin/product_category/add-product-category.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def edit_product_category(request,id):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':

            data=request.POST.copy()

            edit_product_category_url=hosturl+"/api/product/update_product_category"
            edit_product_category_request = requests.post(edit_product_category_url, data=data,headers=headers,files=request.FILES)
            edit_product_category_response = edit_product_category_request.json()
            return HttpResponse(json.dumps(edit_product_category_response),content_type='application/json')
        else:
            data={'id':id}
            get_product_category_details_url=hosturl+"/api/product/product_category_by_id"
            get_product_category_details_request = requests.post(get_product_category_details_url, data=data,headers=headers)
            get_product_category_details_response = get_product_category_details_request.json()
            print("get_product_category_details_response",get_product_category_details_response)
            return render(request, 'admin/product_category/edit-product-category.html',{'product_category':get_product_category_details_response['data']})
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    






# Create your views here.
def product_sub_category_list(request):
    token = request.session.get('token',False)
    if token:
        return render(request, 'admin/product_sub_category/product-sub-category-list.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    

def add_product_sub_category(request):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            print("jii")
            data=request.POST.copy()
            add_product_sub_category_url=hosturl+"/api/product/add_product_subcategory"
            add_product_sub_category_request = requests.post(add_product_sub_category_url, data=data,headers=headers,files=request.FILES)
            add_product_sub_category_response = add_product_sub_category_request.json()
            return HttpResponse(json.dumps(add_product_sub_category_response),content_type='application/json')
        else:
            data=request.POST.copy()

            get_product_category_url=hosturl+"/api/product/product_category_list"
            get_product_category_request = requests.get(get_product_category_url, data=data,headers=headers,files=request.FILES)
            get_product_category_response = get_product_category_request.json()

            return render(request, 'admin/product_sub_category/add-product-sub-category.html',{'categories':get_product_category_response['data']})
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def edit_product_sub_category(request,id):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':

            data=request.POST.copy()
            edit_product_sub_category_url=hosturl+"/api/product/update_product_subcategory"
            edit_product_sub_category_request = requests.post(edit_product_sub_category_url, data=data,headers=headers,files=request.FILES)
            edit_product_sub_category_response = edit_product_sub_category_request.json()
            return HttpResponse(json.dumps(edit_product_sub_category_response),content_type='application/json')
        else:
            data={'id':id}
            get_product_sub_category_details_url=hosturl+"/api/product/product_subcategory_by_id"
            get_product_sub_category_details_request = requests.post(get_product_sub_category_details_url, data=data,headers=headers)
            get_product_sub_category_details_response = get_product_sub_category_details_request.json()
            print("get_product_sub_category_details_response",get_product_sub_category_details_response)

            get_product_category_url=hosturl+"/api/product/product_category_list"
            get_product_category_request = requests.get(get_product_category_url, data=data,headers=headers,files=request.FILES)
            get_product_category_response = get_product_category_request.json()


            return render(request, 'admin/product_sub_category/edit-product-sub-category.html',{'categories':get_product_category_response['data'],'product_sub_category':get_product_sub_category_details_response['data']})
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    