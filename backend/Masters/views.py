from django.shortcuts import render
from rest_framework.authentication import (BaseAuthentication,get_authorization_header)
from rest_framework import permissions
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from .models import *
from .serializers import *

# Create your views here.
class addstate(GenericAPIView):
    # authentication_classes=[userJWTAuthentication]
    # permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        request_data = request.data.copy()
        data['name']=request.data.get('name')
        if data['name'] is None or data['name'] =='':
            return Response({ "data":{},"response":{"n":0,"msg":"Please provide state name", "status":"error"}})
        
        
        data['code']=request.data.get('code')
        if data['code'] is None or data['code'] =='':
            return Response({ "data":{},"response":{"n":0,"msg":"Please provide state code", "status":"error"}})
        
        data['country']=request.data.get('country')
        if data['country'] is None or data['country'] =='':
            return Response({ "data":{},"response":{"n":0,"msg":"Please provide country", "status":"error"}})
        
        data['capital']=request.data.get('capital')
        data['description'] = request.data.get('description')
        data['best_time_to_visit'] = request.data.get('best_time_to_visit')
        data['popular_destinations'] = request.data.get('popular_destinations')
        data['is_active'] = True
        # data['isActive'] = True

        image= request.FILES.get('image')
        if image is not None:
            data['image'] = image

        else:
            data['image'] = None



        already_exist = State.objects.filter(is_active=True, name=data['name']).first()        
        if already_exist is not None:        
            return Response({"data":'',"response": {"n": 0, "msg": "State already exist", "status": "error"}})
        
        else:
            serializer = StateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

                return Response({"data":serializer.data,"response": {"n": 1, "msg": "State added successfully","status":"success"}})
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data" : serializer.errors,"response":{"n":0,"msg":first_key+' : '+ first_value[0],"status":"error"}})  
    


class adddestination(GenericAPIView):
    # authentication_classes=[userJWTAuthentication]
    # permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        request_data = request.data.copy()
        data['name']=request.data.get('name')
        
        
        data['state']=request.data.get('state')
        
        data['destination_type']=request.data.get('destination_type')
        data['description'] = request.data.get('description')
        
        data['latitude']=request.data.get('latitude')
        data['longitude']=request.data.get('longitude')
        data['average_temperature']=request.data.get('average_temperature')
        data['is_popular']=True
        data['best_time_to_visit'] = request.data.get('best_time_to_visit')
        data['is_active'] = True

        # data['isActive'] = True

        image= request.FILES.get('image')
        if image is not None:
            data['image'] = image

        else:
            data['image'] = None



        already_exist = Destination.objects.filter(is_active=True, name=data['name']).first()        
        if already_exist is not None:        
            return Response({"data":'',"response": {"n": 0, "msg": "Destination already exist", "status": "error"}})
        
        else:
            serializer = DestinationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Destination added successfully","status":"success"}})
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data" : serializer.errors,"response":{"n":0,"msg":first_key+' : '+ first_value[0],"status":"error"}})  

class updatedestination(GenericAPIView):
    # authentication_classes=[userJWTAuthentication]
    # permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        data={}
        request_data = request.data.copy()
        data['id']=request.data.get('id')
        data['name']=request.data.get('name')
    
        data['state']=request.data.get('state')
        
        data['destination_type']=request.data.get('destination_type')
        data['description'] = request.data.get('description')
        
        data['latitude']=request.data.get('latitude')
        data['longitude']=request.data.get('longitude')
        data['average_temperature']=request.data.get('average_temperature')
        data['is_popular']=True
        data['best_time_to_visit'] = request.data.get('best_time_to_visit')
        data['is_active'] = True

        # data['isActive'] = True

        image= request.FILES.get('image')
        if image is not None:
            data['image'] = image

        else:
            data['image'] = None


        update_obj=Destination.objects.filter(id=data['id'],is_active=True,).first()
        if update_obj is None:
            return Response({"data":'',"response": {"n": 0, "msg": "Destination not found", "status": "error"}})

        already_exist = Destination.objects.filter(is_active=True, name=data['name']).exclude(id=update_obj.id).first()        
        if already_exist is not None:        
            return Response({"data":'',"response": {"n": 0, "msg": "Destination already exist", "status": "error"}})
        
        else:
            serializer = DestinationSerializer(update_obj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()

                return Response({"data":serializer.data,"response": {"n": 1, "msg": "Destination added successfully","status":"success"}})
            else:
                first_key, first_value = next(iter(serializer.errors.items()))
                return Response({"data" : serializer.errors,"response":{"n":0,"msg":first_key+' : '+ first_value[0],"status":"error"}})  
    

class gethotelslist(GenericAPIView):

    def post(self,request):
        data={}
        request_data = request.data.copy()

        hotels_objs = Hotel.objects.filter(is_active=True)    
        if hotels_objs.exists():
            serializer = HotelSerializer(hotels_objs,many=True)


            return Response({"data":serializer.data,"response": {"n": 1, "msg": "Hotels found successfully","status":"success"}})

        else:
            return Response({"data" : [],"response":{"n":0,"msg":'Hotels not found',"status":"error"}})  




























