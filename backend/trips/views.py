from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import TripPlan, ItineraryItem, TripInvoice
from .serializers import TripPlanSerializer, ItineraryItemSerializer, TripInvoiceSerializer
from User.jwt import userJWTAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def trip_list(request):
    print("hii",)
    """Get all trips for the authenticated user"""
    trips = TripPlan.objects.filter(user=request.user.id).order_by('-created_at')
    serializer = TripPlanSerializer(trips, many=True)
    return Response({
        'data': {'trips': serializer.data},
        'response': {
            'n': 1,
            'msg': 'Trips retrieved successfully',
            'status': 'success'
        }
    })
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def create_trip(request):
    """Create a new trip"""

            
            
   
        



    serializer = TripPlanSerializer(data=request.data)
    if serializer.is_valid():
        trip = serializer.save(user=request.user)
        return Response({
            'data': {'trip_id': trip.id},
            'response': {
                'n': 1,
                'msg': 'Trip created successfully',
                'status': 'success'
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'data': {},
        'response': {
            'n': 0,
            'msg': 'Validation error',
            'status': 'error',
            'errors': serializer.errors
        }
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def trip_detail(request, trip_id):
    """Get trip details with itinerary"""
    print("ola")
    try:
        trip = TripPlan.objects.get(id=trip_id, user=str(request.user.id))
    except TripPlan.DoesNotExist:
        return Response({
            'data': {},
            'response': {
                'n': 0,
                'msg': 'Trip not found',
                'status': 'error'
            }
        }, status=status.HTTP_404_NOT_FOUND)
    
    trip_serializer = TripPlanSerializer(trip)
    itinerary = ItineraryItem.objects.filter(trip=trip).order_by('date', 'time_of_day')
    itinerary_serializer = ItineraryItemSerializer(itinerary, many=True)
    
    return Response({
        'data': {
            'trip': trip_serializer.data,
            'itinerary': itinerary_serializer.data
        },
        'response': {
            'n': 1,
            'msg': 'Trip details retrieved',
            'status': 'success'
        }
    })

@api_view(['POST'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def add_itinerary_item(request):
    """Add an itinerary item to a trip"""
    serializer = ItineraryItemSerializer(data=request.data)
    if serializer.is_valid():
        try:
            trip = TripPlan.objects.get(id=request.data.get('trip_id'), user=request.user)
            item = serializer.save(trip=trip)
            return Response({
                'data': {'item_id': item.id},
                'response': {
                    'n': 1,
                    'msg': 'Itinerary item added successfully',
                    'status': 'success'
                }
            })
        except TripPlan.DoesNotExist:
            return Response({
                'data': {},
                'response': {
                    'n': 0,
                    'msg': 'Trip not found',
                    'status': 'error'
                }
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'data': {},
        'response': {
            'n': 0,
            'msg': 'Validation error',
            'status': 'error',
            'errors': serializer.errors
        }
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_itinerary_item(request, item_id):
    """Delete an itinerary item"""
    try:
        item = ItineraryItem.objects.get(id=item_id, trip__user=request.user)
        item.delete()
        return Response({
            'data': {},
            'response': {
                'n': 1,
                'msg': 'Itinerary item deleted successfully',
                'status': 'success'
            }
        })
    except ItineraryItem.DoesNotExist:
        return Response({
            'data': {},
            'response': {
                'n': 0,
                'msg': 'Item not found',
                'status': 'error'
            }
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes([userJWTAuthentication])
@permission_classes([IsAuthenticated])
def generate_invoice(request, trip_id):
    """Generate invoice for a trip"""
    try:
        trip = TripPlan.objects.get(id=trip_id, user=request.user)
        invoice, created = TripInvoice.objects.get_or_create(trip=trip)
        invoice.generate_invoice()
        
        serializer = TripInvoiceSerializer(invoice)
        return Response({
            'data': {'invoice': serializer.data},
            'response': {
                'n': 1,
                'msg': 'Invoice generated successfully',
                'status': 'success'
            }
        })
        
    except TripPlan.DoesNotExist:
        return Response({
            'data': {},
            'response': {
                'n': 0,
                'msg': 'Trip not found',
                'status': 'error'
            }
        }, status=status.HTTP_404_NOT_FOUND)
        




import google.generativeai as genai
from datetime import datetime, timedelta
import json
import time
# Assuming Django/DRF context from previous files. These imports are needed for the view to function.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

# --- API Key Configuration ---
# CRITICAL: API key MUST be empty for the execution environment to inject the secure token.
GEMINI_API_KEY = "AIzaSyAFRSVeDZVLAUUYaYwlMY2i7E4OYILwlMs" 

# --- Constants for Retry Logic ---
MAX_RETRIES = 5
INITIAL_DELAY = 1  # seconds
# Using the fastest model available for structured JSON output
# FASTEST_MODEL = "gemini-2.5-flash-lite-preview-06-17" 
FASTEST_MODEL = "gemini-2.0-flash"

# --- Gemini Client Helper Functions ---




def get_gemini_model():
    """Initializes and returns the fastest, appropriate GenerativeModel."""
    try:
        # FIX: Explicitly configure the API key for the runtime environment to detect the token.
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
        
        model = genai.GenerativeModel(FASTEST_MODEL)
        print(f"✅ Using fastest model: {FASTEST_MODEL}")
        return model
    except Exception as e:
        print(f"❌ Error initializing Gemini model. Check API client configuration: {e}")
        return None

def ai_trip_plan_gemini(request_data):

    # --- Extract fields ---
    destination = request_data.get('destination')
    budget = request_data.get('budget')
    start_date_str = request_data.get('start_date')
    trip_duration = request_data.get('trip_duration')
    people = request_data.get('people')
    start_location = request_data.get('start_location')

    religion = request_data.get('religion')
    interests = request_data.get('interests')
    stay_options = request_data.get('stay_options')
    travel_category = request_data.get('travel_category')
    travel_mode = request_data.get('travel_mode')

    title = request_data.get('title', 'Generated Trip Plan')

    # --- FIX: Proper missing-field check ---
    if destination is None or budget is None or start_date_str is None or trip_duration is None or people is None:
        return {'error': 'Missing required fields.', 'status_code': 400}

    # Ensure numeric types
    budget = int(budget)
    people = int(people)
    trip_duration = int(trip_duration)

    # --- Generate trip dates ---
    date_list = generate_trip_dates(start_date_str, trip_duration)
    if isinstance(date_list, dict) and 'error' in date_list:
        return date_list

    # Load Gemini model
    model = get_gemini_model()
    if not model:
        return {'error': 'Failed to initialize Gemini model.', 'status_code': 503}
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "budget_summary": {
                "type": "OBJECT",
                "description": "Total estimated costs for the trip. Values MUST be formatted strings with currency and commas (e.g., 'INR 5,000').",
                "properties": {
                    "travel": {"type": "STRING", "description": "Estimated total travel cost (e.g., flights, train)."},
                    "stay": {"type": "STRING", "description": "Estimated total accommodation cost."},
                    "food": {"type": "STRING", "description": "Estimated total food cost."},
                    "activities": {"type": "STRING", "description": "Estimated total activities and entry fees cost."},
                    "grand_total": {"type": "STRING", "description": "The sum of all estimated costs."},
                }
            },
            "ai_suggestions": {
                "type": "ARRAY",
                "items": {"type": "STRING"},
                "description": "Short, practical travel tips or warnings related to the plan."
            },
            "itinerary": {
                "type": "ARRAY",
                "description": f"The detailed daily plan for {trip_duration} days, using the dates: {date_list}",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "title": {"type": "STRING", "description": "e.g., Day 1: Arrival in [City]"},
                        "date": {"type": "STRING", "description": "Use the corresponding date from the provided list."},
                        "description": {"type": "STRING", "description": "Main summary of the day's activities."},
                        "activities": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "category": {"type": "STRING", "description": "e.g., Stay, Food, Local Travel, Activity"},
                                    "details": {"type": "STRING", "description": "Specific detail, e.g., Mid-range hotel for 4 nights, Lunch at local cafe"},
                                    "cost": {"type": "STRING", "description": "Estimated cost for this item (e.g., 'INR 1,500')"}
                                }
                            }
                        },
                        "day_total": {"type": "STRING", "description": "Sum of all costs in activities (e.g., 'INR 5,000')."}
                    },
                },
            },
            "packing_list": {
                "type": "ARRAY",
                "items": {"type": "STRING"},
                "description": "Essential items for the trip based on the destination and estimated weather."
            },
            "transport_options": {
                "type": "ARRAY",
                "description": f"Key transportation options (e.g., Flight, Train, Bus) for {destination}.",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "type": {"type": "STRING", "description": "e.g., Flight, Train, Bus, Car"},
                        "icon": {"type": "STRING", "description": "Font Awesome icon class for the type (e.g., 'fa-plane', 'fa-train', 'fa-bus', 'fa-car')."},
                        "price": {"type": "STRING", "description": "Estimated one-way price for {people} people (e.g., 'INR 8,500')."},
                        "duration": {"type": "STRING", "description": "Estimated travel duration (e.g., '2h 15m', '17h 30m')."},
                    }
                }
            }
        },
        "required": ["itinerary", "budget_summary", "ai_suggestions", "packing_list", "transport_options"]
    }
    
    # Additional user context to make plan more accurate
    extra_factors = f"""
    Religion Preference: {religion}
    User Interests: {interests}
    Preferred Stay Options: {stay_options}
    Travel Category: {travel_category}
    Travel Mode: {travel_mode}
    """

    system_instruction = (
        f"You are an expert travel planner named Stefi Travel AI. Create a {trip_duration}-day itinerary "
        f"for {people} people traveling from {start_location} to {destination}. "
        f"Stay within a total budget of INR {budget}. Return JSON strictly matching the schema."
    )

    prompt = f"""
    {system_instruction}

    --- USER DETAILS ---
    Destination: {destination}
    Duration: {trip_duration} days ({date_list[0]} to {date_list[-1]})
    Travelers: {people}
    Budget: INR {budget}
    Start Location: {start_location}

    {extra_factors}

    Generate the complete structured trip plan now.
    """

    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": response_schema,
    }

    # --- AI Call with Retry ---
    e = None
    for attempt in range(MAX_RETRIES):
        try:
            response = model.generate_content(
                contents=prompt,
                generation_config=generation_config
            )
            plan_json = json.loads(response.text)
            return {'data': plan_json, 'status_code': 200}

        except Exception as ex:
            e = ex
            print(f"Error Attempt {attempt+1}: {ex}")

        if attempt < MAX_RETRIES - 1:
            time.sleep(INITIAL_DELAY * (2 ** attempt))

    return {'error': f'Gemini failed: {e}', 'status_code': 500}


@csrf_exempt
@api_view(['POST'])
def ai_trip_plan_view(request):
    """
    Django view that receives trip parameters and calls the Gemini AI planner.
    """
    if request.method == 'POST':
        try:
            request_data = request.data
            print("request_data",request_data)
            result = ai_trip_plan_gemini(request_data)
            
            if result['status_code'] == 200:
                return Response({
                    'success': True,
                    'message': 'Trip plan generated successfully.',
                    'trip_plan': result['data']
                }, status=200)
            else:
                return Response({
                    'success': False,
                    'message': result['error']
                }, status=result['status_code'])
                
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Internal server error: {e}'
            }, status=500)
            
    return Response({'success': False, 'message': 'Invalid request method.'}, status=405)


def generate_trip_dates(start_date_str, trip_duration_str):
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        trip_duration_int = int(trip_duration_str)
        date_list = [(start_date + timedelta(days=i)).strftime('%d %b %Y')
                     for i in range(trip_duration_int)]
        return date_list
    except Exception as e:
        return {'error': f'Invalid date or duration: {e}', 'status_code': 400}
