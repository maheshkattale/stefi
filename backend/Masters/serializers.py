from rest_framework import serializers
from .models import (
    TravelCategory, State, Destination, 
    TravelAgency, TravelClass, Hotel, RoomType
)
from django.utils import timezone

class TravelCategorySerializer(serializers.ModelSerializer):
    category_type_display = serializers.CharField(source='get_category_type_display', read_only=True)
    
    class Meta:
        model = TravelCategory
        fields = [
            'id', 'name', 'category_type', 'category_type_display', 
            'description', 'icon', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = [
            'id', 'name', 'code', 'country', 'capital', 'description',
            'image', 'popular_destinations', 'best_time_to_visit',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_code(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("State code cannot exceed 10 characters.")
        return value.upper()

class DestinationSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    state_code = serializers.CharField(source='state.code', read_only=True)
    destination_type_display = serializers.CharField(source='get_destination_type_display', read_only=True)
    
    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'state', 'state_name', 'state_code', 'destination_type',
            'destination_type_display', 'description', 'latitude', 'longitude',
            'best_time_to_visit', 'average_temperature', 'image', 'is_popular',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class TravelAgencySerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    agency_type_display = serializers.CharField(source='get_agency_type_display', read_only=True)
    
    class Meta:
        model = TravelAgency
        fields = [
            'id', 'name', 'agency_type', 'agency_type_display', 'description',
            'contact_person', 'email', 'phone', 'address', 'city', 'state', 'state_name',
            'website', 'rating', 'license_number', 'is_verified', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'rating']
    
    def validate_phone(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Please enter a valid phone number.")
        return value
    
    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value

class TravelClassSerializer(serializers.ModelSerializer):
    class_type_display = serializers.CharField(source='get_class_type_display', read_only=True)
    
    class Meta:
        model = TravelClass
        fields = [
            'id', 'name', 'class_type', 'class_type_display', 'description',
            'amenities', 'price_multiplier', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_price_multiplier(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price multiplier must be greater than 0.")
        return value

class HotelSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    state_name = serializers.CharField(source='destination.state.name', read_only=True)
    hotel_type_display = serializers.CharField(source='get_hotel_type_display', read_only=True)
    star_rating_display = serializers.CharField(source='get_star_rating_display', read_only=True)
    
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'hotel_type', 'hotel_type_display', 'destination', 'destination_name',
            'state_name', 'address', 'contact_email', 'contact_phone', 'star_rating',
            'star_rating_display', 'description', 'amenities', 'check_in_time', 'check_out_time',
            'has_swimming_pool', 'has_spa', 'has_gym', 'has_restaurant', 'wifi_available',
            'parking_available', 'image', 'website', 'average_price_per_night', 'rating',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'rating']
    
    def validate_contact_phone(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Please enter a valid phone number.")
        return value

class RoomTypeSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    destination_name = serializers.CharField(source='hotel.destination.name', read_only=True)
    
    class Meta:
        model = RoomType
        fields = [
            'id', 'name', 'hotel', 'hotel_name', 'destination_name', 'description',
            'max_occupancy', 'base_price', 'amenities', 'size', 'bed_type',
            'is_available', 'image'
        ]
        read_only_fields = ['id']
    
    def validate_base_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Base price must be greater than 0.")
        return value

# Nested Serializers for detailed views
class DestinationDetailSerializer(DestinationSerializer):
    state = StateSerializer(read_only=True)

class HotelDetailSerializer(HotelSerializer):
    destination = DestinationSerializer(read_only=True)

class TravelAgencyDetailSerializer(TravelAgencySerializer):
    state = StateSerializer(read_only=True)

class RoomTypeDetailSerializer(RoomTypeSerializer):
    hotel = HotelSerializer(read_only=True)

# List serializers with minimal fields for dropdowns
class TravelCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelCategory
        fields = ['id', 'name', 'category_type']

class StateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'code']

class DestinationListSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    
    class Meta:
        model = Destination
        fields = ['id', 'name', 'state', 'state_name']

class TravelAgencyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelAgency
        fields = ['id', 'name', 'agency_type', 'city']

class TravelClassListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelClass
        fields = ['id', 'name', 'class_type', 'price_multiplier']

class HotelListSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'destination', 'destination_name', 'star_rating']