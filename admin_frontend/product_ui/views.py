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
    

# Create your views here.
def product_brand_list(request):
    token = request.session.get('token',False)
    if token:

        return render(request, 'admin/product_brand/product-brand-list.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def add_product_brand(request):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            print("jii")
            data=request.POST.copy()
            add_product_brand_url=hosturl+"/api/product/add_product_brand"

            add_product_brand_request = requests.post(add_product_brand_url, data=data,headers=headers,files=request.FILES)
            add_product_brand_response = add_product_brand_request.json()
            return HttpResponse(json.dumps(add_product_brand_response),content_type='application/json')
        else:
            return render(request, 'admin/product_brand/add-product-brand.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def edit_product_brand(request,id):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':

            data=request.POST.copy()

            edit_product_brand_url=hosturl+"/api/product/update_product_brand"
            edit_product_brand_request = requests.post(edit_product_brand_url, data=data,headers=headers,files=request.FILES)
            edit_product_brand_response = edit_product_brand_request.json()
            return HttpResponse(json.dumps(edit_product_brand_response),content_type='application/json')
        else:
            data={'id':id}
            get_product_brand_details_url=hosturl+"/api/product/product_brand_by_id"
            get_product_brand_details_request = requests.post(get_product_brand_details_url, data=data,headers=headers)
            get_product_brand_details_response = get_product_brand_details_request.json()
            print("get_product_brand_details_response",get_product_brand_details_response)
            return render(request, 'admin/product_brand/edit-product-brand.html',{'product_brand':get_product_brand_details_response['data']})
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    



def product_size_list(request):
    token = request.session.get('token',False)
    if token:

        return render(request, 'admin/product_size/product-size-list.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def add_product_size(request):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            print("jii")
            data=request.POST.copy()
            add_product_size_url=hosturl+"/api/product/add_product_size_unit"

            add_product_size_request = requests.post(add_product_size_url, data=data,headers=headers,files=request.FILES)
            add_product_size_response = add_product_size_request.json()
            return HttpResponse(json.dumps(add_product_size_response),content_type='application/json')
        else:
            return render(request, 'admin/product_size/add-product-size.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def edit_product_size(request,id):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            data=request.POST.copy()
            edit_product_size_url=hosturl+"/api/product/update_product_size_unit"
            edit_product_size_request = requests.post(edit_product_size_url, data=data,headers=headers,files=request.FILES)
            edit_product_size_response = edit_product_size_request.json()
            return HttpResponse(json.dumps(edit_product_size_response),content_type='application/json')
        else:
            data={'id':id}
            get_product_size_details_url=hosturl+"/api/product/product_size_unit_by_id"
            get_product_size_details_request = requests.post(get_product_size_details_url, data=data,headers=headers)
            get_product_size_details_response = get_product_size_details_request.json()
            print("get_product_size_details_response",get_product_size_details_response)
            return render(request, 'admin/product_size/edit-product-size.html',{'product_size':get_product_size_details_response['data']})
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    

def product_color_list(request):
    token = request.session.get('token',False)
    if token:

        return render(request, 'admin/product_color/product-color-list.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def add_product_color(request):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            print("jii")
            data=request.POST.copy()
            add_product_color_url=hosturl+"/api/product/add_product_color"

            add_product_color_request = requests.post(add_product_color_url, data=data,headers=headers,files=request.FILES)
            add_product_color_response = add_product_color_request.json()
            return HttpResponse(json.dumps(add_product_color_response),content_type='application/json')
        else:
            return render(request, 'admin/product_color/add-product-color.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def edit_product_color(request,id):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            data=request.POST.copy()
            edit_product_color_url=hosturl+"/api/product/update_product_color"
            edit_product_color_request = requests.post(edit_product_color_url, data=data,headers=headers,files=request.FILES)
            edit_product_color_response = edit_product_color_request.json()
            return HttpResponse(json.dumps(edit_product_color_response),content_type='application/json')
        else:
            data={'id':id}
            get_product_color_details_url=hosturl+"/api/product/product_color_by_id"
            get_product_color_details_request = requests.post(get_product_color_details_url, data=data,headers=headers)
            get_product_color_details_response = get_product_color_details_request.json()
            print("get_product_color_details_response",get_product_color_details_response)
            return render(request, 'admin/product_color/edit-product-color.html',{'product_color':get_product_color_details_response['data']})
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    



def product_list(request):
    token = request.session.get('token',False)
    if token:

        return render(request, 'admin/product/product-list.html')
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def add_product(request):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            print("jii")
            data=request.POST.copy()
            add_product_url=hosturl+"/api/product/add_product"

            add_product_request = requests.post(add_product_url, data=data,headers=headers,files=request.FILES)
            add_product_response = add_product_request.json()
            return HttpResponse(json.dumps(add_product_response),content_type='application/json')
        else:
            data={}
            get_product_category_list_url=hosturl+"/api/product/product_category_list"
            get_product_category_list_request = requests.get(get_product_category_list_url, data=data,headers=headers)
            get_product_category_list_response = get_product_category_list_request.json()

            # print("get_product_category_list_response",get_product_category_list_response['data'])
            get_product_brand_list_url=hosturl+"/api/product/product_brand_list"
            get_product_brand_list_request = requests.get(get_product_brand_list_url, data=data,headers=headers)
            get_product_brand_list_response = get_product_brand_list_request.json()
            # print("get_product_brand_list_response",get_product_brand_list_response)

            get_product_color_list_url=hosturl+"/api/product/product_color_list"
            get_product_color_list_request = requests.get(get_product_color_list_url, data=data,headers=headers)
            get_product_color_list_response = get_product_color_list_request.json()
            # print("get_product_color_list_response",get_product_color_list_response)

            get_product_size_unit_list_url=hosturl+"/api/product/product_size_unit_list"
            get_product_size_unit_list_request = requests.get(get_product_size_unit_list_url, data=data,headers=headers)
            get_product_size_unit_list_response = get_product_size_unit_list_request.json()

            # print("get_product_size_unit_list_response",get_product_size_unit_list_response)
            get_vendors_list_url=hosturl+"/api/vendor/vendor_list"
            get_vendors_list_request = requests.get(get_vendors_list_url, data=data,headers=headers)
            get_vendors_list_response = get_vendors_list_request.json()


            return render(request, 'admin/product/add-product.html',{
                                                                    'category_list':get_product_category_list_response['data'],
                                                                     'brand_list':get_product_brand_list_response['data'],
                                                                     'color_list':get_product_color_list_response['data'],
                                                                     'size_units':get_product_size_unit_list_response['data'],
                                                                     'vendors':get_vendors_list_response['data'],
                                                                    })
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    
def edit_product(request,id):
    token = request.session.get('token',False)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        if request.method == 'POST':
            data=request.POST.copy()
            edit_product_url=hosturl+"/api/product/update_product"
            edit_product_request = requests.post(edit_product_url, data=data,headers=headers,files=request.FILES)
            edit_product_response = edit_product_request.json()
            return HttpResponse(json.dumps(edit_product_response),content_type='application/json')
        else:
            data={'id':id}
            get_product_details_url=hosturl+"/api/product/product_by_id"
            get_product_details_request = requests.post(get_product_details_url, data=data,headers=headers)
            get_product_details_response = get_product_details_request.json()
            print("get_product_details_response",get_product_details_response)

            get_product_category_list_url=hosturl+"/api/product/product_category_list"
            get_product_category_list_request = requests.get(get_product_category_list_url, data=data,headers=headers)
            get_product_category_list_response = get_product_category_list_request.json()

            get_product_subcategory_list_url=hosturl+"/api/product/product_subcategory_list"
            get_product_subcategory_list_request = requests.get(get_product_subcategory_list_url, data=data,headers=headers)
            get_product_subcategory_list_response = get_product_subcategory_list_request.json()

            # print("get_product_category_list_response",get_product_category_list_response['data'])
            get_product_brand_list_url=hosturl+"/api/product/product_brand_list"
            get_product_brand_list_request = requests.get(get_product_brand_list_url, data=data,headers=headers)
            get_product_brand_list_response = get_product_brand_list_request.json()
            # print("get_product_brand_list_response",get_product_brand_list_response)

            get_product_color_list_url=hosturl+"/api/product/product_color_list"
            get_product_color_list_request = requests.get(get_product_color_list_url, data=data,headers=headers)
            get_product_color_list_response = get_product_color_list_request.json()
            # print("get_product_color_list_response",get_product_color_list_response)

            get_product_size_unit_list_url=hosturl+"/api/product/product_size_unit_list"
            get_product_size_unit_list_request = requests.get(get_product_size_unit_list_url, data=data,headers=headers)
            get_product_size_unit_list_response = get_product_size_unit_list_request.json()

            # print("get_product_size_unit_list_response",get_product_size_unit_list_response)
            get_vendors_list_url=hosturl+"/api/vendor/vendor_list"
            get_vendors_list_request = requests.get(get_vendors_list_url, data=data,headers=headers)
            get_vendors_list_response = get_vendors_list_request.json()









            return render(request, 'admin/product/edit-product.html',{
                                                                    'product':get_product_details_response['data'],
                                                                    'category_list':get_product_category_list_response['data'],
                                                                    'brand_list':get_product_brand_list_response['data'],
                                                                    'color_list':get_product_color_list_response['data'],
                                                                    'size_units':get_product_size_unit_list_response['data'],
                                                                    'vendors':get_vendors_list_response['data'],
                                                                    'subcategory_list':get_product_subcategory_list_response['data'],

                })
    else:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('Frontend_User:login') # change this.
    







































