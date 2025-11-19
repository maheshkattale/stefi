from django.shortcuts import render
from rest_framework.authentication import (BaseAuthentication,get_authorization_header)
from rest_framework import permissions
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from .models import *
from .serializers import *
from helpers.custom_functions import *
from django.db.models import F, FloatField, ExpressionWrapper,Q
from User.jwt import userJWTAuthentication

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




class hotel_list_pagination_api(GenericAPIView):
    # authentication_classes=[userJWTAuthentication]
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    # serializer_class = reviews_and_ratingsSerializer

    def post(self,request):
        hotels_objs = Hotel.objects.filter(is_active=True).order_by('-id')
        search = request.data.get('search').strip() if request.data.get('search') else None
        if search is not None and search != '':
            hotels_objs = hotels_objs.filter(Q(name__icontains=search) | Q(hotel_type__icontains=search)).order_by('-id')

        page4 = self.paginate_queryset(hotels_objs)
        serializer = HotelSerializer(page4,many=True)
        return self.get_paginated_response(serializer.data)


class addhotel(GenericAPIView):
    authentication_classes = [userJWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data.copy()
        
        # ✅ Validation for required fields
        required_fields = ['name', 'hotel_type', 'destination', 'address', 'contact_email', 'contact_phone']
        for field in required_fields:
            if not data.get(field):
                return Response({"data": {}, "response": {"n": 0, "msg": f"Please provide {field}", "status": "error"}})
        
        # ✅ Check if hotel exists
        existing_hotel = Hotel.objects.filter(
            name__iexact=data['name'], destination_id=data['destination'], is_active=True
        ).first()
        if existing_hotel:
            return Response({"data": {}, "response": {"n": 0, "msg": "Hotel already exists", "status": "error"}})
        
        # ✅ Create Hotel
        serializer = HotelSerializer(data=data)
        if serializer.is_valid():
            hotel = serializer.save()

            # ✅ Optional: Handle multiple room types from frontend
            room_types = request.data.getlist('room_types[]')
            for room_data in room_types:
                RoomType.objects.create(
                    hotel=hotel,
                    name=room_data.get('name'),
                    description=room_data.get('description', ''),
                    max_occupancy=room_data.get('max_occupancy', 2),
                    base_price=room_data.get('base_price', 0),
                    amenities=room_data.get('amenities', ''),
                    size=room_data.get('size', ''),
                    bed_type=room_data.get('bed_type', ''),
                    is_available=room_data.get('is_available', True),
                )

            return Response({"data": serializer.data, "response": {"n": 1, "msg": "Hotel added successfully!", "status": "success"}})
        else:
            first_key, first_value = next(iter(serializer.errors.items()))
            return Response({"data": serializer.errors, "response": {"n": 0, "msg": f"{first_key}: {first_value[0]}", "status": "error"}})





class get_hotel_types(GenericAPIView):
    def post(self,request):
        hotel_types = [{'key': ht[0], 'value': ht[1]} for ht in Hotel.HOTEL_TYPES]
        return Response({"data": hotel_types, "response": {"n": 1, "msg": "Hotel types fetched successfully", "status": "success"}})

class get_destinations(GenericAPIView):
    def post(self,request):
        destinations_objs = Destination.objects.filter(is_active=True)    
        if destinations_objs.exists():
            serializer = DestinationSerializer(destinations_objs,many=True)
            return Response({"data":serializer.data,"response": {"n": 1, "msg": "Destinations found successfully","status":"success"}})
        else:
            return Response({"data" : [],"response":{"n":0,"msg":'Destinations not found',"status":"error"}})













