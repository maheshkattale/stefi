from rest_framework import serializers
from .models import TripPlan, ItineraryItem, TripInvoice

class ItineraryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryItem
        fields = '__all__'
        read_only_fields = ['id', 'total_cost']

# class TripPlanSerializer(serializers.ModelSerializer):
#     itinerary = ItineraryItemSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = TripPlan
#         fields = '__all__'
#         read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
#     def create(self, validated_data):
#         validated_data['user'] = self.context['request'].user
#         return super().create(validated_data)

class TripInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripInvoice
        fields = '__all__'
        read_only_fields = ['id', 'invoice_number', 'issue_date', 'subtotal', 'tax_amount', 'total_amount']

from rest_framework import serializers
from .models import TripPlan
from datetime import date

class TripPlanSerializer(serializers.ModelSerializer):
    currency = serializers.ChoiceField(
        choices=[
            ('INR', 'Indian Rupee (₹)'),
            ('USD', 'US Dollar ($)'),
            ('EUR', 'Euro (€)'),
            ('GBP', 'British Pound (£)'),
        ],
        default='INR',
        required=False
    )
    
    class Meta:
        model = TripPlan
        fields = "__all__"
    
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("End date cannot be before start date.")
        
        if start_date and start_date < date.today():
            raise serializers.ValidationError("Start date cannot be in the past.")
        
        return data
    
    def validate_persons(self, value):
        if value < 1:
            raise serializers.ValidationError("Number of travelers must be at least 1.")
        if value > 20:
            raise serializers.ValidationError("Maximum 20 travelers allowed per trip.")
        return value
    
    def validate_budget(self, value):
        if value < 0:
            raise serializers.ValidationError("Budget cannot be negative.")
        return value