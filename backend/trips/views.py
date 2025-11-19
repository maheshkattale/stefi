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
        


# from datetime import datetime, timedelta
# # The following imports are retained from your context for the combined file
# import json
# import time # Added for exponential backoff delay
# from google import genai
# from google.genai.errors import APIError

# # --- API Key Configuration ---
# # NOTE: The API key is now set to an empty string as required for reliable execution
# # in this environment. The actual key is supplied securely at runtime.
# GEMINI_API_KEY = "AIzaSyB1kWojp8hF4IDUv_tWz1UrtMensTQ6Lnc" # Updated for stable environment execution

# # --- Constants for Retry Logic ---
# MAX_RETRIES = 5
# INITIAL_DELAY = 1 # seconds

# # --- Gemini Client Helper Functions ---

# def get_gemini_client():
#     """Initializes and returns the Gemini API client."""
#     try:
#         # Use the global empty key. The runtime environment handles insertion.
#         client = genai.Client(api_key=globals()['GEMINI_API_KEY'])
#         return client
#     except Exception as e:
#         print(f"Error initializing Gemini client: {e}")
#         return None

# def ai_trip_plan_gemini(request_data):
#     """
#     Generates a detailed travel plan using the Gemini API, enforcing a structured JSON output.
#     Now includes exponential backoff for resilient API calls.
#     """
    
#     destination = request_data.get('destination')
#     budget = request_data.get('budget')
#     start_date_str = request_data.get('start_date')
#     trip_duration = request_data.get('trip_duration')
#     people = request_data.get('people')
#     start_location = request_data.get('start_location')

#     print("request_data",request_data)
#     # Basic input validation
#     if not all([destination, budget, start_date_str, trip_duration, people]):
#         return {
#             'error': 'Missing required fields: destination, budget, start_date, duration, or people.',
#             'status_code': 400
#         }
    
#     # Calculate the actual end date string for better planning context
#     try:

#         # Generate placeholder dates for the itinerary planning based on the start date
#         date_list=generate_trip_dates(start_date_str, trip_duration)
#         print("date_list",date_list)
#     except ValueError:
#         return {
#             'error': 'Invalid date format provided.',
#             'status_code': 400
#         }
    
#     print("10")
#     client = get_gemini_client()
#     if not client:
#         return {
#             'error': 'AI service not initialized. Check the API key configuration.',
#             'status_code': 503
#         }

#     # --- JSON Schema Definition (MUST match frontend requirements) ---
#     response_schema = {
#         "type": "OBJECT",
#         "properties": {
#             "budget_summary": {
#                 "type": "OBJECT",
#                 "description": "Total estimated costs for the trip. Values MUST be formatted strings with currency and commas (e.g., 'INR 5,000').",
#                 "properties": {
#                     "travel": {"type": "STRING", "description": "Estimated total travel cost (e.g., flights, train)."},
#                     "stay": {"type": "STRING", "description": "Estimated total accommodation cost."},
#                     "food": {"type": "STRING", "description": "Estimated total food cost."},
#                     "activities": {"type": "STRING", "description": "Estimated total activities and entry fees cost."},
#                     "grand_total": {"type": "STRING", "description": "The sum of all estimated costs."},
#                 }
#             },
#             "ai_suggestions": {
#                 "type": "ARRAY",
#                 "items": {"type": "STRING"},
#                 "description": "Short, practical travel tips or warnings related to the plan."
#             },
#             "itinerary": {
#                 "type": "ARRAY",
#                 "description": f"The detailed daily plan for {trip_duration} days, using the dates: {date_list}",
#                 "items": {
#                     "type": "OBJECT",
#                     "properties": {
#                         "title": {"type": "STRING", "description": "e.g., Day 1: Arrival in [City]"},
#                         "date": {"type": "STRING", "description": "Use the corresponding date from the provided list."},
#                         "description": {"type": "STRING", "description": "Main summary of the day's activities."},
#                         "activities": {
#                             "type": "ARRAY",
#                             "items": {
#                                 "type": "OBJECT",
#                                 "properties": {
#                                     "category": {"type": "STRING", "description": "e.g., Stay, Food, Local Travel, Activity"},
#                                     "details": {"type": "STRING", "description": "Specific detail, e.g., Mid-range hotel for 4 nights, Lunch at local cafe"},
#                                     "cost": {"type": "STRING", "description": "Estimated cost for this item (e.g., 'INR 1,500')"}
#                                 }
#                             }
#                         },
#                         "day_total": {"type": "STRING", "description": "Sum of all costs in activities (e.g., 'INR 5,000')."}
#                     },
#                 },
#             },
#             "packing_list": {
#                 "type": "ARRAY",
#                 "items": {"type": "STRING"},
#                 "description": "Essential items for the trip based on the destination and estimated weather."
#             },
#             "transport_options": {
#                 "type": "ARRAY",
#                 "description": f"Key transportation options (e.g., Flight, Train, Bus) for {destination}.",
#                 "items": {
#                     "type": "OBJECT",
#                     "properties": {
#                         "type": {"type": "STRING", "description": "e.g., Flight, Train, Bus, Car"},
#                         "icon": {"type": "STRING", "description": "Font Awesome icon class for the type (e.g., 'fa-plane', 'fa-train', 'fa-bus', 'fa-car')."},
#                         "price": {"type": "STRING", "description": "Estimated one-way price for {people} people (e.g., 'INR 8,500')."},
#                         "duration": {"type": "STRING", "description": "Estimated travel duration (e.g., '2h 15m', '17h 30m')."},
#                     }
#                 }
#             }
#         },
#         "required": ["itinerary", "budget_summary", "ai_suggestions", "packing_list", "transport_options"]
#     }

#     # 1. Define a clear System Instruction
#     system_instruction = (
#         "You are an expert travel planner named Stefi Travel AI. Create a comprehensive, "
#         f"{trip_duration}-day travel itinerary and related data for {destination}. "
#         "The plan must strictly adhere to the user's total budget. "
#         "The output must be a valid JSON object matching the provided schema. "
#         "Ensure all costs are accurate estimations for the trip and are provided as formatted strings with currency symbols and commas (e.g., 'INR 1,500')."
#     )

#     # 2. Construct the user prompt
#     prompt = f"""
#     Generate a complete travel plan named '{start_location}' for {people} people to {destination}.
#     Total Budget (Maximum): {budget} INR.
#     Trip Duration: {trip_duration} days, starting from {start_date_str}.

#     Please ensure the detailed daily itinerary is well-paced, realistic, and the estimated total cost stays close to or below the maximum budget.
#     """

#     # 3. Call the Gemini API with Exponential Backoff
#     for attempt in range(MAX_RETRIES):
#         try:
#             response = client.models.generate_content(
#                 model='gemini-2.5-flash-preview-05-20',
#                 contents=prompt,
#                 config={
#                     'system_instruction': system_instruction,
#                     'response_mime_type': 'application/json',
#                     'response_schema': response_schema,
#                 },
#             )
            
#             # If successful, process and return the JSON
#             plan_json = json.loads(response.text)
#             return {
#                 'data': plan_json,
#                 'status_code': 200
#             }

#         except APIError as e:
#             # Check if this is a retriable error (like a rate limit or transient 5xx)
#             # The genai library handles most transient errors gracefully, but we add a manual backoff
#             # for robustness against service-side rate limiting or temporary issues.
#             print(f"Gemini API Error (Attempt {attempt + 1}/{MAX_RETRIES}): {e}")
#             if attempt < MAX_RETRIES - 1:
#                 delay = INITIAL_DELAY * (2 ** attempt)
#                 print(f"Retrying in {delay} seconds...")
#                 time.sleep(delay)
#             else:
#                 # Last attempt failed
#                 return {
#                     'error': f'AI generation failed after {MAX_RETRIES} attempts due to an API issue: {e}',
#                     'status_code': 500
#                 }
#         except json.JSONDecodeError:
#             # If the model returns malformed JSON, this is usually a failure on the model's side,
#             # but retrying might help if it was a truncation error.
#             print(f"JSON Decode Error (Attempt {attempt + 1}/{MAX_RETRIES}). Raw response: {response.text}")
#             if attempt < MAX_RETRIES - 1:
#                 delay = INITIAL_DELAY * (2 ** attempt)
#                 print(f"Retrying in {delay} seconds...")
#                 time.sleep(delay)
#             else:
#                  return {
#                     'error': 'AI generated an invalid JSON response after retries. Please try again.',
#                     'status_code': 500
#                 }
#         except Exception as e:
#             # Catches other unexpected errors
#             print(f"Unexpected error: {e}")
#             return {
#                 'error': f'An unexpected server error occurred: {e}',
#                 'status_code': 500
#             }

#     # Should be unreachable, but included for safety
#     return {
#         'error': 'Exited retry loop without success.',
#         'status_code': 500
#     }

# # --- Django REST Framework View ---

# @csrf_exempt
# @api_view(['POST'])
# def ai_trip_plan_view(request):
#     """
#     Django view that receives trip parameters and calls the Gemini AI planner.
#     """
#     if request.method == 'POST':
#         try:
#             # The JSON payload is automatically parsed by DRF when using @api_view
#             request_data = request.data
            
#             # Use the helper function
#             result = ai_trip_plan_gemini(request_data)
            
#             if result['status_code'] == 200:
#                 # Success: Return the AI-generated structured data
#                 return Response({
#                     'success': True,
#                     'message': 'Trip plan generated successfully.',
#                     'trip_plan': result['data']
#                 }, status=200)
#             else:
#                 # Error: Return the error message and status code
#                 return Response({
#                     'success': False,
#                     'message': result['error']
#                 }, status=result['status_code'])
                
#         except Exception as e:
#             return Response({
#                 'success': False,
#                 'message': f'Internal server error: {e}'
#             }, status=500)
            
#     return Response({'success': False, 'message': 'Invalid request method.'}, status=405)

# def generate_trip_dates(start_date_str, trip_duration_str):
#     """
#     Generates a list of date strings for the trip duration.

#     Args:
#         start_date_str (str): The start date in 'YYYY-MM-DD' format.
#         trip_duration_str (str): The duration of the trip as a string (e.g., '3').

#     Returns:
#         list[str] or dict: List of formatted dates or an error dictionary.
#     """
#     try:
#         # 1. Convert the start date string to a datetime object
#         start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        
#         # 2. CRITICAL FIX: Convert the trip duration string to an integer
#         # If the conversion fails (e.g., if trip_duration_str is 'abc'),
#         # it will be caught by the ValueError block below.
#         trip_duration_int = int(trip_duration_str)

#         # Generate placeholder dates for the itinerary planning
#         # The range() function now correctly receives an integer.
#         date_list = [
#             (start_date + timedelta(days=i)).strftime('%d %b %Y')
#             for i in range(trip_duration_int)
#         ]
        
#         return date_list

#     except ValueError as e:
#         # This catches errors from both strptime (invalid date format)
#         # and int() (invalid number format for duration)
#         print(f"Error during date/duration parsing: {e}")
#         return {
#             'error': 'Invalid date or duration format provided. Duration must be a whole number.',
#             'status_code': 400
#         }


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
GEMINI_API_KEY = "AIzaSyBwk4Cbpry0HarnRPe-v316aKfAn8EtdYo" 

# --- Constants for Retry Logic ---
MAX_RETRIES = 5
INITIAL_DELAY = 1  # seconds
# Using the fastest model available for structured JSON output
# FASTEST_MODEL = "gemini-2.5-flash-lite-preview-06-17" 
FASTEST_MODEL = "gemini-2.5-flash-preview-05-20"

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
    destination = request_data.get('destination')
    budget = request_data.get('budget')
    start_date_str = request_data.get('start_date')
    trip_duration = request_data.get('trip_duration')
    people = request_data.get('people')
    start_location = request_data.get('start_location')
    title = request_data.get('title', 'Generated Trip Plan')

    if not all([destination, budget, start_date_str, trip_duration, people]):
        return {'error': 'Missing required fields.', 'status_code': 400}

    date_list = generate_trip_dates(start_date_str, trip_duration)
    if isinstance(date_list, dict) and 'error' in date_list:
        return date_list

    model = get_gemini_model()
    if not model:
        return {'error': 'Failed to initialize Gemini model. Check API key/quotas.', 'status_code': 503}
    
    # --- JSON Schema Definition (REQUIRED for structured output) ---
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
    
    # --- Configuration for System Instruction ---
    system_instruction = (
        f"You are an expert travel planner named Stefi Travel AI. Create a detailed {trip_duration}-day itinerary "
        f"for {people} people traveling from {start_location} to {destination}. The plan is named '{title}'. "
        f"Stay within a total budget of INR {budget}. Return output as valid JSON strictly matching the schema. "
        f"Ensure all costs are accurate estimations and provided as formatted strings with currency symbols and commas (e.g., 'INR 1,500')."
    )

    # --- Configuration for Structured Output (generation_config) ---
    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": response_schema,
    }

    # FIX: Prepending system_instruction content to the prompt to ensure the model follows instructions.
    prompt = f"""
    {system_instruction}

    --- USER QUERY ---

    Destination: {destination}
    Duration: {trip_duration} days ({date_list[0]} to {date_list[-1]})
    Travelers: {people}
    Budget: INR {budget}
    Starting Location: {start_location}
    Generate the complete, structured trip plan now.
    """

    e = None 

    # Retry loop with exponential backoff for resilience
    for attempt in range(MAX_RETRIES):
        try:
            # FIX: Only passing contents and generation_config
            response = model.generate_content(
                contents=prompt, 
                generation_config=generation_config,
            )

            text = response.text.strip()
            plan_json = json.loads(text) 
            return {'data': plan_json, 'status_code': 200}

        except json.JSONDecodeError:
            print(f"JSON Decode Error (Attempt {attempt + 1}/{MAX_RETRIES}). Retrying...")
            e = Exception("Invalid JSON from Model")
        except Exception as ex:
            e = ex
            # APIError is caught here, including 429 Quota Exceeded.
            print(f"Gemini API Error (Attempt {attempt + 1}/{MAX_RETRIES}): {e}")

        if attempt < MAX_RETRIES - 1:
            delay = INITIAL_DELAY * (2 ** attempt)
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            break

    # Final fallback after all attempts
    return {'error': f'Gemini failed after {MAX_RETRIES} attempts. Please check API quotas and key validity: {e}', 'status_code': 500}


# --- Django REST Framework View (Re-inserted for completeness) ---

@csrf_exempt
@api_view(['POST'])
def ai_trip_plan_view(request):
    """
    Django view that receives trip parameters and calls the Gemini AI planner.
    """
    if request.method == 'POST':
        try:
            request_data = request.data
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
